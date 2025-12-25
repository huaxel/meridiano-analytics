<script>
    import "@evidence-dev/tailwind/fonts.css";
    import "../app.css";
    import { EvidenceDefaultLayout } from "@evidence-dev/core-components";
    import { base } from "$app/paths";
    export let data;
</script>

<EvidenceDefaultLayout {data} logo="{base}/meridiano.jpg">
    <slot slot="content" />
</EvidenceDefaultLayout>
