import {defineConfig} from 'vite';
import plugin from '@revideo/vite-plugin';

// `@revideo/vite-plugin` is CommonJS, so an ESM default import lands on the
// module object rather than the function on some setups. Unwrapping it here is
// the difference between a dev server and "motionCanvas is not a function".
const motionCanvas = (plugin as any).default ?? plugin;

// The renderer serves this project through vite and drives it in a headless
// browser, so the config has to exist even though nobody opens it by hand.
export default defineConfig({
  plugins: [motionCanvas({project: ['./project.ts']})],
  server: {port: 9001, strictPort: false},
});
