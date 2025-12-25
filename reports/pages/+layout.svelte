<script>
    import "@evidence-dev/tailwind/fonts.css";
    import "../app.css";
    import { EvidenceDefaultLayout } from "@evidence-dev/core-components";
    import { base } from "$app/paths";
    export let data;
</script>

<svelte:head>
    <link rel="icon" href="{base}/favicon.ico" sizes="any" />
    <link rel="icon" type="image/png" href="{base}/icon.png" />
    <link rel="apple-touch-icon" href="{base}/apple-touch-icon.png" />
</svelte:head>

<EvidenceDefaultLayout {data} logo="{base}/meridiano.jpg">
    <slot slot="content" />

    <div
        slot="footer"
        class="mt-12 py-6 border-t border-gray-200 text-center text-xs text-gray-400 font-mono"
    >
        <p>© 2024 Banco Meridiano de Inversión S.A.</p>
        <p>
            Departamento de Remuneraciones | Última actualización: {new Date().toLocaleDateString()}
        </p>
        <div class="mt-2 flex justify-center gap-4 opacity-50">
            <span>Confidencial</span>
            <span>Uso Interno</span>
        </div>
    </div>
</EvidenceDefaultLayout>
