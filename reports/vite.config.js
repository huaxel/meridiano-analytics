import { defineConfig } from 'vite'

export default defineConfig({
    server: {
        // 1. Listen on all addresses (replaces --host)
        host: "0.0.0.0", 
        // 2. Allow your Tailscale domain
        allowedHosts: [
            "framearch-juan.bonobo-fort.ts.net"
        ]
    }
})
