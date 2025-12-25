<script>
    import "@evidence-dev/tailwind/fonts.css";
    import "../app.css";
    import { EvidenceDefaultLayout } from "@evidence-dev/core-components";
    import { base } from "$app/paths";
    export let data;
</script>

<svelte:head>
    <link rel="icon" href="{base}/favicon.ico" />
    <link rel="apple-touch-icon" href="{base}/apple-touch-icon.png" />
</svelte:head>

<EvidenceDefaultLayout {data} logo="{base}/meridiano.jpg">
    <slot slot="content" />
</EvidenceDefaultLayout>
