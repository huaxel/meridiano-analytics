const evidenceTailwind = require('@evidence-dev/tailwind/config').config;

/** @type {import("tailwindcss").Config} */
module.exports = {
	presets: [evidenceTailwind],
	content: {
		relative: true,
		files: [
			'./pages/**/*.{html,js,svelte,ts,md}',
			'./components/**/*.{html,js,svelte,ts,md}',
            './node_modules/@evidence-dev/core-components/dist/**/*.{html,js,svelte,ts,md}'
		]
	},
	theme: {
		extend: {}
	}
};
