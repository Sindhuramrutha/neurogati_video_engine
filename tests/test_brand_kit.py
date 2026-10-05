"""Brand assets: a watermark, a logo, an intro and an outro. Stored by content,
placed and timed by numbers a person set, transferred with Assets & Design, and
put on by the render exactly as the page previews them."""

# ruff: noqa: F811
import io
import shutil
import subprocess

import pytest
from PIL import Image

from pipeline import operations
from pipeline.assets_handoff import (
    ConfirmedAssetStore,
    assets_page,
    brand_for_later_stages,
    confirm_assets,
    fingerprint,
)
from pipeline.brand_kit import (
    BrandFile,
    BrandKit,
    BrandKitStore,
    ClipEdit,
    Placement,
    remove_brand_file,
    set_brand_options,
    store_brand_file,
)
from pipeline.brand_overlay import overlay_box, prepare_overlay
from pipeline.operations import OperationFailed
from pipeline.render_brand import brand_arguments
from tests.test_assets_and_export import (  # noqa: F401
    picture_bytes,
    project_root,
)

HAS_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


def _video(path, seconds=1, audio=True, colour="red"):
    arguments = ["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
                 f"color=c={colour}:s=320x240:d={seconds}:r=30"]
    if audio:
        arguments += ["-f", "lavfi", "-i", f"sine=f=440:d={seconds}"]
    subprocess.run([*arguments, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-shortest", str(path)],
                   check=True)
    return path.read_bytes()


def solid_png(colour, size=(200, 100)):
    buffer = io.BytesIO()
    Image.new("RGBA", size, colour).save(buffer, "PNG")
    return buffer.getvalue()


# --- storing ---------------------------------------------------------------------------


def test_a_logo_is_stored_by_its_content_and_measured(project_root):
    slug = operations.create_project("Brand")["slug"]
    page = store_brand_file(slug, "logo", "my logo.png", picture_bytes(size=(300, 200)))
    logo = page["kit"]["logo"]
    assert (logo["width"], logo["height"]) == (300, 200)
    assert logo["file_name"] == "my logo.png"
    again = store_brand_file(slug, "logo", "renamed.png", picture_bytes(size=(300, 200)))
    assert again["kit"]["logo"]["path"] == logo["path"], "same bytes, same stored file"


def test_unusable_brand_files_are_refused(project_root):
    slug = operations.create_project("Refuse")["slug"]
    with pytest.raises(OperationFailed, match="at least"):
        store_brand_file(slug, "logo", "dot.png", picture_bytes(size=(20, 20)))
    with pytest.raises(OperationFailed, match="must be one of"):
        store_brand_file(slug, "intro", "intro.png", picture_bytes())
    with pytest.raises(OperationFailed, match="not a brand asset"):
        store_brand_file(slug, "banner", "b.png", picture_bytes())


# --- placing -----------------------------------------------------------------------------


def test_a_placement_is_set_field_by_field_and_kept_inside_its_limits(project_root):
    slug = operations.create_project("Place")["slug"]
    store_brand_file(slug, "logo", "logo.png", solid_png("red"))

    view = set_brand_options(slug, {"logo_place": {"x": 0.25, "y": 0.75, "width": 0.2,
                                                   "opacity": 0.5, "radius": 0.3}})
    place = view["kit"]["logo_place"]
    assert (place["x"], place["y"], place["width"], place["opacity"], place["radius"]) == (
        0.25, 0.75, 0.2, 0.5, 0.3)

    dragged = set_brand_options(slug, {"logo_place": {"width": 9, "opacity": -1, "x": 4}})
    place = dragged["kit"]["logo_place"]
    assert (place["width"], place["opacity"], place["x"]) == (0.6, 0.05, 1.0), \
        "past the end of a slider saves its end"
    assert place["y"] == 0.75, "what was not sent is not changed"

    with pytest.raises(OperationFailed):
        set_brand_options(slug, {"logo_place": {"colour": "red"}})
    with pytest.raises(OperationFailed):
        set_brand_options(slug, {"banner_place": {"x": 0.5}})


def test_when_it_shows_is_a_window_inside_the_lesson():
    lesson = 60.0
    assert Placement().window(lesson) == (0.0, 60.0)
    assert Placement(show="first", seconds=8).window(lesson) == (0.0, 8.0)
    assert Placement(show="last", seconds=8).window(lesson) == (52.0, 60.0)
    assert Placement(show="range", start=10, end=25).window(lesson) == (10.0, 25.0)
    assert Placement(show="range", start=50, end=90).window(lesson) == (50.0, 60.0), \
        "never past the lesson's end"
    assert Placement(show="first", seconds=300).window(lesson) == (0.0, 60.0)


def test_an_older_kit_keeps_its_logo_exactly_where_it_was():
    """A kit saved with 'top right, medium' is read as the same pixels."""
    older = BrandKit.model_validate({
        "logo": {"path": "assets/brand/l.png", "width": 200, "height": 100},
        "logo_corner": "top-right", "logo_size": "medium", "watermark_opacity": "light"})
    box = overlay_box(older.logo, older.logo_place)
    assert box["width_px"] == 173, "9% of 1920"
    assert (box["left_px"], box["top_px"]) == (1920 - 173 - 48, 48), "48 px in from the corner"
    assert older.watermark_place.opacity == 0.18 and older.watermark_place.width == 0.40


def test_trims_and_cross_fades_decide_where_the_lesson_starts():
    intro = BrandFile(path="i.mp4", duration_ms=10_000)
    kit = BrandKit(intro=intro, outro=BrandFile(path="o.mp4", duration_ms=6_000),
                   intro_edit=ClipEdit(trim_start=1, trim_end=2, fade=1.5),
                   outro_edit=ClipEdit(fade=1))
    assert kit.intro_seconds == 7.0
    assert kit.lesson_starts_at_ms == 5500, "7 s of intro, less the 1.5 s they overlap"
    assert kit.total_ms(60_000) == 5500 + 60_000 + 5000
    assert ClipEdit(trim_start=50, trim_end=50).length(intro) == 0.5, "never trimmed away"
    assert ClipEdit(fade=2).overlap(BrandFile(duration_ms=2000)) == 1.0, "half the clip at most"


# --- the overlay is the preview and the render ---------------------------------------------


def test_the_overlay_is_drawn_once_with_its_size_corners_opacity_and_shadow(project_root):
    slug = operations.create_project("Overlay")["slug"]
    project = operations.require_project(slug)
    store_brand_file(slug, "logo", "logo.png", solid_png((255, 0, 0, 255), (200, 100)))
    kit = BrandKitStore(project.root).load()

    plain = Placement(width=0.1, opacity=0.5)
    overlay = prepare_overlay(project.root, kit.logo, plain)
    with Image.open(overlay) as image:
        assert image.size == (192, 96), "10% of the frame wide, its own proportions"
        assert image.getpixel((96, 48)) == (255, 0, 0, 128), "half as opaque"
    assert prepare_overlay(project.root, kit.logo, plain) == overlay, "same settings, same file"

    rounded = prepare_overlay(project.root, kit.logo, Placement(width=0.1, radius=0.5))
    with Image.open(rounded) as image:
        assert image.getpixel((0, 0))[3] == 0 and image.getpixel((96, 48))[3] == 255

    shadowed = Placement(width=0.1, shadow=1.0)
    with Image.open(prepare_overlay(project.root, kit.logo, shadowed)) as image:
        assert image.size == (192 + 2 * 17, 96 + 2 * 17), "room for the shadow around it"
    box = overlay_box(kit.logo, shadowed)
    assert box["left_px"] == round(0.5 * 1920 - 96) - 17, "the picture stays where it was put"

    page = assets_page(slug)["brand"]
    assert page["overlays"]["logo"]["file"].endswith(".png"), "the page shows the same file"


def test_the_command_places_times_trims_and_fades_by_the_kits_numbers(project_root, tmp_path):
    slug = operations.create_project("Command")["slug"]
    project = operations.require_project(slug)
    store_brand_file(slug, "logo", "logo.png", solid_png("red"))
    kit = BrandKitStore(project.root).load()
    kit.logo_place = Placement(x=0.5, y=0.5, width=0.1, show="range", start=2, end=8,
                               fade_in=1, fade_out=1)
    kit.intro = BrandFile(path="assets/brand/i.mp4", duration_ms=5000)
    kit.intro_edit = ClipEdit(trim_start=1, fade=1)

    arguments = brand_arguments(kit, project.root, tmp_path / "lesson.mp4",
                                tmp_path / "out.mp4", lesson_seconds=20.0)
    graph = arguments[arguments.index("-filter_complex") + 1]
    assert "overlay=x=864:y=492:enable='between(t,2.000,8.000)'" in graph, "centred, 2 s to 8 s"
    assert "fade=t=in:st=2.000:d=1.000:alpha=1" in graph
    assert "fade=t=out:st=7.000:d=1.000:alpha=1" in graph
    assert "trim=start=1.000:end=5.000" in graph, "one second off the intro's start"
    assert "anullsrc" in " ".join(arguments), "a silent intro gets silence"
    assert "xfade=transition=fade:duration=1.000:offset=3.000" in graph, "4 s of intro, 1 s shared"
    assert arguments == brand_arguments(kit, project.root, tmp_path / "lesson.mp4",
                                        tmp_path / "out.mp4", lesson_seconds=20.0)


# --- the transfer -----------------------------------------------------------------------------


def test_the_kit_reaches_the_render_only_once_transferred(project_root):
    slug = operations.create_project("Handoff brand")["slug"]
    project = operations.require_project(slug)
    store_brand_file(slug, "watermark", "wm.png", picture_bytes())
    assert assets_page(slug)["handoff"]["pending"] is True

    confirm_assets(slug)   # a kit alone can be transferred: no pictures needed
    assert brand_for_later_stages(project).watermark is not None
    assert assets_page(slug)["handoff"]["pending"] is False

    set_brand_options(slug, {"watermark_place": {"opacity": 0.4}})
    assert brand_for_later_stages(project).watermark_place.opacity == 0.10, "not until transferred"
    assert assets_page(slug)["handoff"]["pending"] is True, "moving a slider is a change to hand on"

    remove_brand_file(slug, "watermark")
    confirm_assets(slug)
    assert ConfirmedAssetStore(project.root).load().brand.is_empty


def test_an_empty_kit_leaves_earlier_fingerprints_alone(project_root):
    from pipeline.assets import AssetLibrary

    library = AssetLibrary()
    assert fingerprint(library) == fingerprint(library, BrandKit())


# --- a real render ------------------------------------------------------------------------------


def _frame(video, at_seconds, target):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{at_seconds}", "-i", str(video),
                    "-frames:v", "1", str(target)], check=True)
    with Image.open(target) as image:
        return image.convert("RGB").copy()


@pytest.mark.skipif(not HAS_FFMPEG, reason="needs ffmpeg")
def test_the_brand_pass_puts_the_logo_where_and_when_it_was_set(project_root, tmp_path):
    from pipeline.render_brand import apply_brand
    from pipeline.speech import measure_audio_duration_ms

    slug = operations.create_project("Brand run")["slug"]
    project = operations.require_project(slug)
    store_brand_file(slug, "logo", "logo.png", solid_png((0, 255, 0, 255), (200, 200)))
    store_brand_file(slug, "intro", "intro.mp4", _video(tmp_path / "i.mp4", 3, audio=False,
                                                        colour="blue"))
    store_brand_file(slug, "outro", "outro.mp4", _video(tmp_path / "o.mp4", 2, colour="white"))
    set_brand_options(slug, {
        "logo_place": {"x": 0.25, "y": 0.25, "width": 0.2, "show": "first", "seconds": 2},
        "intro_edit": {"trim_start": 1, "fade": 1},      # 2 s of intro, 1 s shared
        "outro_edit": {"fade": 0}})
    confirm_assets(slug)
    kit = brand_for_later_stages(project)

    lesson = tmp_path / "video.mp4"
    _video(lesson, 4, colour="red")
    working = tmp_path / "work"
    working.mkdir()
    apply_brand(kit, project.root, lesson, working)

    # 2 s intro + 4 s lesson - 1 s shared + 2 s outro.
    assert 6800 <= measure_audio_duration_ms(lesson) <= 7300
    assert kit.lesson_starts_at_ms == 1000

    # The lesson starts at 1 s: the logo is on from 1 s to 3 s of the video.
    at_logo = (round(0.25 * 1920), round(0.25 * 1080))
    during = _frame(lesson, 2.5, tmp_path / "during.png").getpixel(at_logo)
    after = _frame(lesson, 4.0, tmp_path / "after.png").getpixel(at_logo)
    assert during[1] > 200 and during[0] < 80, f"the green logo is there at 2.5 s: {during}"
    assert after[0] > 200 and after[1] < 80, f"and gone, the red lesson showing, at 4 s: {after}"
    # (The 4:3 test clip is letterboxed to x 240..1680; 1500 is inside the picture.)
    outside = _frame(lesson, 2.5, tmp_path / "outside.png").getpixel((1500, 900))
    assert outside[0] > 200 and outside[1] < 80, "and only where it was put"
