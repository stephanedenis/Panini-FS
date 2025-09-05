import { getCurrentRoute, onRouteChange } from './router'
import { createMd, rewriteLinks } from './markdown'

type Root = { base: string; root: string }
type AppConfig = { roots: Root[] }

const md = createMd()
const app = document.getElementById('app')!

async function loadConfig(): Promise<AppConfig> {
  const res = await fetch('/config.json')
  const cfg = await res.json()
  return cfg
}

function resolveCandidates(roots: Root[], path: string) {
  const candidates: string[] = []
  const p = path.replace(/\/$/, '') || '/'
  for (const r of roots) {
    const prefix = r.root.replace(/\/$/, '')
    const base = p === '/' ? '/index' : p
    candidates.push(`${prefix}${base}.md`)
    candidates.push(`${prefix}${p}/index.md`)
  }
  return candidates
}

async function loadMarkdown(roots: Root[], routePath: string): Promise<string> {
  const cands = resolveCandidates(roots, routePath)
  for (const url of cands) {
    try {
      const res = await fetch(url, { cache: 'no-cache' })
      if (res.ok) return await res.text()
    } catch {}
  }
  return `# 404 — Not found\n\nAucun document pour \`${routePath}\``
}

async function renderRoute(cfg: AppConfig) {
  const { path } = getCurrentRoute()
  const mdSrc = await loadMarkdown(cfg.roots, path)
  const html = md.render(mdSrc)
  app.innerHTML = html
  rewriteLinks(app)
  const h1 = app.querySelector('h1')?.textContent?.trim()
  if (h1) document.title = `${h1} — OntoWave`
}

;(async () => {
  const cfg = await loadConfig()
  await renderRoute(cfg)
  onRouteChange(() => renderRoute(cfg))
})()
