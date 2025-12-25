<script>
    import "@evidence-dev/tailwind/fonts.css";
    import "../app.css";
    import { EvidenceDefaultLayout } from "@evidence-dev/core-components";
    import { base } from "$app/paths";
    export let data;
</script>

<EvidenceDefaultLayout {data} logo="{base}/meridiano.jpg">
    <svelte:head>
        <link rel="icon" href="{base}/favicon.ico" />
        <link rel="apple-touch-icon" href="{base}/apple-touch-icon.png" />
    </svelte:head>
    <slot slot="content" />
</EvidenceDefaultLayout>
