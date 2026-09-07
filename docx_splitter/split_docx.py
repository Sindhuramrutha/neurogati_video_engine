import re
import shutil
import zipfile
from copy import deepcopy
from pathlib import Path

from lxml import etree


# ============================================================
# PATH CONFIGURATION
# ============================================================

# Script location:
#
# C:\Users\DELL\Desktop\neurogati_video_engine\docx_splitter\
#
BASE_DIR = Path(__file__).resolve().parent

# Big source DOCX files
BIG_DOC_FOLDER = BASE_DIR / "big_doc"

# Local split output
SUBMODULE_FOLDER = BASE_DIR / "submodules"

# Video engine
VIDEO_ENGINE_FOLDER = BASE_DIR.parent

# NPS input folder
NPS_INPUT_FOLDER = (
    VIDEO_ENGINE_FOLDER
    / "projects"
    / "NPS"
    / "input_files"
)


# ============================================================
# OPTIONS
# ============================================================

# False = existing section files are skipped
# True  = existing section files are recreated
#
# Keep this False for normal use.
#
FORCE_REBUILD = False


# ============================================================
# DOCX XML NAMESPACES
# ============================================================

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
}

W_BODY = f"{{{NS['w']}}}body"
W_P = f"{{{NS['w']}}}p"
W_SECT_PR = f"{{{NS['w']}}}sectPr"


# ============================================================
# SECTION DETECTION
# ============================================================

# Detect headings like:
#
# 4.1 Introduction
# 4.2 Neural Signals
# 6.1 Why Neural Signals Change with Time
#
SECTION_RE = re.compile(
    r"^\s*(\d+\.\d+)\s+(.+?)\s*$"
)


def get_paragraph_text(paragraph):
    """
    Get all visible text from a Word paragraph.

    This combines all w:t elements inside the paragraph.
    """

    texts = paragraph.xpath(
        ".//w:t/text()",
        namespaces=NS
    )

    return "".join(texts).strip()


def find_section_heading(element):
    """
    Check whether an XML element is a section heading.

    Returns:

        ("6.1", "Why Neural Signals Change with Time")

    or None.
    """

    if element.tag != W_P:
        return None

    text = get_paragraph_text(element)

    match = SECTION_RE.match(text)

    if not match:
        return None

    section_number = match.group(1)
    title = match.group(2).strip()

    return section_number, title


# ============================================================
# SAFE FILENAME
# ============================================================

def safe_filename(text):
    """
    Make a Windows-safe filename.
    """

    text = re.sub(
        r'[<>:"/\\|?*]',
        "",
        text
    )

    text = re.sub(
        r"\s+",
        "_",
        text
    )

    return text.strip("_")


# ============================================================
# CREATE SECTION DOCX
# ============================================================

def create_section_docx(
    source_docx,
    output_docx,
    start_index,
    end_index,
    body_elements
):
    """
    Create a new DOCX containing the selected section.

    IMPORTANT:

    We copy the original DOCX package rather than rebuilding
    paragraphs with python-docx.

    This preserves:

        - images
        - JPEG
        - JPG
        - PNG
        - formula images
        - tables
        - formatting
        - relationships
        - embedded objects
        - styles
        - numbering
        - fonts
        - media
    """

    # --------------------------------------------------------
    # Read the original document.xml
    # --------------------------------------------------------

    with zipfile.ZipFile(
        source_docx,
        "r"
    ) as source_zip:

        document_xml = source_zip.read(
            "word/document.xml"
        )

        document_tree = etree.fromstring(
            document_xml
        )

        body = document_tree.find(
            W_BODY
        )

        if body is None:
            raise RuntimeError(
                "Could not find document body."
            )

        # ----------------------------------------------------
        # Preserve sectPr
        #
        # Word requires sectPr to remain the final
        # child of <w:body>.
        # ----------------------------------------------------

        sect_pr = body.find(
            W_SECT_PR
        )

        if sect_pr is not None:

            body.remove(
                sect_pr
            )

        # ----------------------------------------------------
        # Remove all existing body content
        # ----------------------------------------------------

        for child in list(body):

            body.remove(
                child
            )

        # ----------------------------------------------------
        # Add selected section elements
        # ----------------------------------------------------

        selected_elements = body_elements[
            start_index:end_index
        ]

        for element in selected_elements:

            body.append(
                deepcopy(element)
            )

        # ----------------------------------------------------
        # Add original sectPr back
        # ----------------------------------------------------

        if sect_pr is not None:

            body.append(
                deepcopy(sect_pr)
            )

        # ----------------------------------------------------
        # Convert XML back to bytes
        # ----------------------------------------------------

        new_document_xml = etree.tostring(
            document_tree,
            xml_declaration=True,
            encoding="UTF-8",
            standalone="yes"
        )

        # ----------------------------------------------------
        # Create new DOCX
        #
        # We copy the ENTIRE original DOCX package.
        #
        # This is important because it keeps:
        #
        # word/media/*
        # word/_rels/*
        # word/styles.xml
        # word/numbering.xml
        # etc.
        #
        # Therefore images and formulas remain available.
        # ----------------------------------------------------

        with zipfile.ZipFile(
            output_docx,
            "w",
            zipfile.ZIP_DEFLATED
        ) as output_zip:

            for item in source_zip.infolist():

                # Replace document.xml
                if item.filename == "word/document.xml":

                    output_zip.writestr(
                        item,
                        new_document_xml
                    )

                else:

                    output_zip.writestr(
                        item,
                        source_zip.read(
                            item.filename
                        )
                    )


# ============================================================
# PROCESS ONE MODULE
# ============================================================

def split_module(input_file):

    module_name = input_file.stem

    # --------------------------------------------------------
    # Local output
    #
    # submodules/Module_6/
    # --------------------------------------------------------

    local_module_folder = (
        SUBMODULE_FOLDER
        / module_name
    )

    local_module_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # NPS module name
    #
    # Module_6 → Module-6
    # --------------------------------------------------------

    nps_module_name = module_name.replace(
        "_",
        "-"
    )

    nps_module_folder = (
        NPS_INPUT_FOLDER
        / nps_module_name
    )

    nps_module_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    print()
    print("=" * 70)
    print(
        f"PROCESSING: {input_file.name}"
    )
    print("=" * 70)

    print()
    print("Source:")
    print(
        f"  {input_file}"
    )

    print()
    print("Local output:")
    print(
        f"  {local_module_folder}"
    )

    print()
    print("NPS output:")
    print(
        f"  {nps_module_folder}"
    )

    print()

    # ========================================================
    # READ DOCX XML
    # ========================================================

    with zipfile.ZipFile(
        input_file,
        "r"
    ) as source_zip:

        document_xml = source_zip.read(
            "word/document.xml"
        )

    document_tree = etree.fromstring(
        document_xml
    )

    body = document_tree.find(
        W_BODY
    )

    if body is None:

        print(
            "ERROR: Could not find Word document body."
        )

        return

    # --------------------------------------------------------
    # Get direct body elements
    # --------------------------------------------------------

    body_elements = list(body)

    # --------------------------------------------------------
    # Find section headings
    # --------------------------------------------------------

    headings = []

    for index, element in enumerate(
        body_elements
    ):

        heading = find_section_heading(
            element
        )

        if heading:

            section_number, title = heading

            headings.append(
                {
                    "index": index,
                    "number": section_number,
                    "title": title
                }
            )

    # ========================================================
    # NO SECTIONS
    # ========================================================

    if not headings:

        print()
        print(
            "ERROR: NO SECTIONS FOUND"
        )

        print()
        print(
            "Your DOCX should contain headings like:"
        )

        print()
        print(
            "6.1 Why Neural Signals Change with Time"
        )

        print(
            "6.2 Short-Time Fourier Transform"
        )

        print()

        return

    print(
        f"Found {len(headings)} sections."
    )

    print()

    created_count = 0
    skipped_count = 0
    copied_count = 0

    # ========================================================
    # PROCESS EACH SECTION
    # ========================================================

    for position, section in enumerate(
        headings
    ):

        number = section["number"]
        title = section["title"]

        start_index = section["index"]

        # ----------------------------------------------------
        # End of current section
        # ----------------------------------------------------

        if position + 1 < len(headings):

            end_index = headings[
                position + 1
            ]["index"]

        else:

            # Last section goes until the end
            end_index = len(
                body_elements
            )

        # ----------------------------------------------------
        # Filename
        # ----------------------------------------------------

        filename = (
            f"{number}_"
            f"{safe_filename(title)}"
            f".docx"
        )

        # ----------------------------------------------------
        # Output locations
        # ----------------------------------------------------

        local_file = (
            local_module_folder
            / filename
        )

        nps_file = (
            nps_module_folder
            / filename
        )

        # ====================================================
        # LOCAL FILE
        # ====================================================

        if (
            local_file.exists()
            and not FORCE_REBUILD
        ):

            print(
                f"SKIP - already exists:"
            )

            print(
                f"  {local_file.name}"
            )

            skipped_count += 1

        else:

            # ------------------------------------------------
            # Create section DOCX
            # ------------------------------------------------

            create_section_docx(
                source_docx=input_file,
                output_docx=local_file,
                start_index=start_index,
                end_index=end_index,
                body_elements=body_elements
            )

            print(
                "CREATED:"
            )

            print(
                f"  {local_file.name}"
            )

            print(
                "  ✓ Images/formulas preserved"
            )

            created_count += 1

        # ====================================================
        # NPS COPY
        # ====================================================

        if (
            nps_file.exists()
            and not FORCE_REBUILD
        ):

            print(
                "  NPS copy already exists"
            )

        else:

            shutil.copy2(
                local_file,
                nps_file
            )

            print(
                "  COPIED TO NPS:"
            )

            print(
                f"    {nps_file}"
            )

            copied_count += 1

        print()

    # ========================================================
    # MODULE COMPLETE
    # ========================================================

    print(
        "-" * 70
    )

    print(
        f"Module complete: {module_name}"
    )

    print(
        f"Created: {created_count}"
    )

    print(
        f"Skipped: {skipped_count}"
    )

    print(
        f"Copied to NPS: {copied_count}"
    )

    print(
        "-" * 70
    )


# ============================================================
# FIND ALL MODULE DOCX FILES
# ============================================================

def find_all_input_docx():

    BIG_DOC_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    return sorted(
        BIG_DOC_FOLDER.glob("*.docx")
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("DOCX MODULE SPLITTER")
    print("=" * 70)

    # --------------------------------------------------------
    # Find all big module DOCX files
    # --------------------------------------------------------

    docx_files = find_all_input_docx()

    if not docx_files:

        print()
        print(
            "ERROR: NO DOCX FILES FOUND"
        )

        print()
        print(
            "Put your module DOCX files here:"
        )

        print()
        print(
            BIG_DOC_FOLDER
        )

        print()

        return

    # --------------------------------------------------------
    # Show files
    # --------------------------------------------------------

    print()
    print(
        f"Found {len(docx_files)} module DOCX file(s):"
    )

    print()

    for file in docx_files:

        print(
            f"  - {file.name}"
        )

    print()

    # ========================================================
    # PROCESS EVERY MODULE
    # ========================================================

    for input_file in docx_files:

        split_module(
            input_file
        )

    # ========================================================
    # COMPLETE
    # ========================================================

    print()
    print("=" * 70)
    print("ALL MODULES COMPLETE")
    print("=" * 70)

    print()
    print(
        "Local submodules:"
    )

    print(
        f"  {SUBMODULE_FOLDER}"
    )

    print()

    print(
        "NPS video engine input:"
    )

    print(
        f"  {NPS_INPUT_FOLDER}"
    )

    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()