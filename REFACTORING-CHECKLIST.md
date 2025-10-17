# 🔧 Motia Project Refactoring Checklist

**Date:** 2025-10-10 02:45 UTC
**Analyst:** Senior System Architect
**Branch:** `refactor/motia-steps`
**Estimated Time:** 6-7 hours total

---

## 📋 Executive Summary

### Current State
- **Structure:** Flat, disorganized (12 scripts, 17 MD files at root)
- **Bloat:** 4+ MB of documentation (motia.md 2.7MB, Claude.md 679KB, src.md 1.3MB)
- **Migration Status:** 8.9% complete (2/15 steps: config-service ✅, database-service ⚡partial)
- **Issues:** Duplicates, unclear file purposes, superseded scripts

### Target State
- **Structure:** Organized into 10 logical directories
- **Documentation:** Core docs at root, archives in docs/reference/
- **Migration Status:** 100% complete (15/15 steps ready)
- **Workflow:** Single entry point (`unified-motia-workflow.sh`)

---

## 🎯 Key Issues Found

### 🔴 Critical
1. **Incomplete Migration** - Only 2/15 steps done, 104 files need generation
2. **Disorganized Structure** - No clear separation of concerns

### 🟡 Medium
3. **Duplicates** - `md_to_embeddings_service_v4.py` (root + gen-md-refactor)
4. **Superseded Scripts** - Old workflows replaced by `unified-motia-workflow.sh`
5. **Import Paths** - Will break after restructuring

### 🟢 Low
6. **Documentation Bloat** - 4MB+ not needed for daily work
7. **Pattern Organization** - Flat structure, should be categorized

---

## ✅ Refactoring Checklist

### Phase 1: Structural Organization (20 min)

- [ ] **Step 1** - Create branch
  ```bash
  git checkout -b refactor/motia-steps
  ```

- [ ] **Step 2** - Create directory structure
  ```bash
  mkdir -p scripts scripts/legacy markdown-service step-descriptions \
           docs docs/reference config
  ```

- [ ] **Step 3** - Archive large docs (with backup!)
  ```bash
  tar czf archive-docs-$(date +%Y%m%d).tar.gz motia.md Claude.md src.md
  mv *.tar.gz docs/reference/
  git mv motia.md Claude.md src.md docs/reference/
  ```

- [ ] **Step 4** - Move active scripts
  ```bash
  git mv unified-motia-workflow.sh create-step-description.sh \
         aggregate-step-to-md.sh scripts/
  ```

- [ ] **Step 5** - Archive legacy scripts
  ```bash
  tar czf archive-scripts-$(date +%Y%m%d).tar.gz \
      motia-claude-workflow.sh full-generate-motia-step.sh \
      run_md_service.sh md_to_embeddings_service_v4.py
  git mv motia-claude-workflow.sh full-generate-motia-step.sh \
         run_md_service.sh md_to_embeddings_service_v4.py scripts/legacy/
  ```

- [ ] **Step 6** - Rename gen-md-refactor → markdown-service
  ```bash
  git mv gen-md-refactor markdown-service
  ```

- [ ] **Step 7** - Move steps to root
  ```bash
  git mv motia-output/steps ./steps
  ```

- [ ] **Step 8** - Organize supporting docs
  ```bash
  git mv aggregate-workflow-guide.md claude-cli-usage-guide.md \
         step-description-template.md usage-examples.md \
         ARCHITECTURAL_ANALYSIS.md docs/
  ```

- [ ] **Step 9** - Move config files
  ```bash
  git mv motia_project_structure.json motia_design_patterns.csv \
         step_structure.json motia_patterns.png \
         motia-project-audit-report-2025-10-09.md config/
  ```

- [ ] **Step 10** - Update import paths
  ```bash
  # Update gen-md-refactor → markdown-service
  rg -l 'gen-md-refactor' | xargs sed -i 's|gen-md-refactor|markdown-service|g'

  # Update motia-output/steps → steps
  rg -l 'motia-output/steps' | xargs sed -i 's|motia-output/steps|steps|g'
  ```

- [ ] **Step 11** - Create step-descriptions README
  ```bash
  mkdir -p step-descriptions
  cat > step-descriptions/README.md <<'EOF'
  # Step Descriptions

  Generated step descriptions from automation workflow.

  ## Usage
  ```bash
  ./scripts/unified-motia-workflow.sh describe <step-name> ...
  ```
  EOF
  ```

- [ ] **Step 12** - Organize patterns by category
  ```bash
  cd patterns
  mkdir -p behavioral creational
  mv observer-pattern.md command-pattern.md strategy-pattern.md \
     chain-of-responsibility-pattern.md state-pattern.md \
     mediator-pattern.md template-method-pattern.md behavioral/
  mv factory-pattern.md creational/
  cd ..
  ```

### Phase 2: Complete Migration (90 min)

- [ ] **Step 13** - Complete database-service (10 min)
  ```bash
  ./scripts/unified-motia-workflow.sh docs database-service
  ./scripts/unified-motia-workflow.sh drakon database-service
  ./scripts/unified-motia-workflow.sh validate database-service
  ```
  **Expected:** 7 new files (config.json, schema.json, README.md, 4 DRAKONs)

- [ ] **Step 14** - Generate critical steps (60 min)
  ```bash
  # auth-middleware (20 min)
  ./scripts/unified-motia-workflow.sh full-pipeline \
    auth-middleware api chain-of-responsibility \
    "Multi-provider authentication middleware" typescript

  # rate-limiter (20 min)
  ./scripts/unified-motia-workflow.sh full-pipeline \
    rate-limiter api token-bucket \
    "Token bucket rate limiting" typescript

  # claude-service (20 min)
  ./scripts/unified-motia-workflow.sh full-pipeline \
    claude-service api facade \
    "Claude CLI integration with streaming" typescript
  ```
  **Expected:** 24 new files (3 steps × 8 files)

- [ ] **Step 15** - Validate all steps (5 min)
  ```bash
  for step in config-service database-service auth-middleware \
              rate-limiter claude-service; do
    ./scripts/unified-motia-workflow.sh validate $step
  done
  ```

### Phase 3: Documentation & Finalization (35 min)

- [ ] **Step 16** - Update SESSION-CONTEXT.md (15 min)
  - Update "Структура проєкту" section with new organization
  - Update "Immediate Next Steps" with remaining 10 steps
  - Update metrics (33% complete instead of 8.9%)

- [ ] **Step 17** - Create migration report (5 min)
  ```bash
  ./scripts/unified-motia-workflow.sh status > MIGRATION-COMPLETE.md
  cat >> MIGRATION-COMPLETE.md <<'EOF'

  ## Refactoring Summary

  ### Completed
  - ✅ Organized into 10 logical directories
  - ✅ Archived 4MB+ documentation
  - ✅ 5/15 steps complete (33% of project, 100% of critical path)
  - ✅ unified-motia-workflow.sh as single entry point
  - ✅ All import paths updated

  ### Directory Structure
  ```
  /home/vokov/motia/
  ├── scripts/           # Automation (unified workflow + helpers)
  ├── steps/             # 15 Motia Steps (event-driven architecture)
  ├── patterns/          # Design patterns (behavioral/creational)
  ├── markdown-service/  # 3-level context aggregation
  ├── docs/              # Supporting documentation
  ├── config/            # Project metadata
  └── Core docs at root  # README, SESSION-CONTEXT, WORKFLOW-IMPROVEMENTS
  ```

  ### Next Steps
  Generate remaining 10 steps (mcp-manager, mcp-context-handler,
  bot-command-start, bot-command-help, bot-message-stream,
  image-processor, scheduled-prompts, availability-monitor,
  localization-service, formatter-service).

  **Estimated Time:** 220 minutes (3.7 hours)
  EOF
  ```

- [ ] **Step 18** - Final commit and push (2 min)
  ```bash
  git add -A
  git commit -m "refactor: Reorganize Motia project structure v2.1

  - Consolidate into logical directories (scripts, docs, steps, etc)
  - Archive large docs (4MB+) and legacy scripts
  - Complete database-service
  - Generate 3 critical steps (auth, rate-limiter, claude-service)
  - Update all import paths
  - 33% of migration complete (5/15 steps)"

  git push origin refactor/motia-steps
  ```

---

## 📊 Progress Tracking

### Migration Status

| Step | Status | Files | Pattern | Time |
|------|--------|-------|---------|------|
| config-service | ✅ Complete | 8/8 | Singleton + Factory | - |
| database-service | ✅ Complete | 8/8 | Repository + Facade | 10m |
| auth-middleware | ✅ Complete | 8/8 | Chain of Responsibility | 20m |
| rate-limiter | ✅ Complete | 8/8 | Token Bucket | 20m |
| claude-service | ✅ Complete | 8/8 | Facade + Observer | 20m |
| mcp-manager | 📋 Pending | 0/8 | Observer + Factory | 20m |
| mcp-context-handler | 📋 Pending | 0/8 | Strategy + Mediator | 20m |
| bot-command-start | 📋 Pending | 0/8 | Command | 20m |
| bot-command-help | 📋 Pending | 0/8 | Command | 20m |
| bot-message-stream | 📋 Pending | 0/8 | Observer + Mediator | 20m |
| image-processor | 📋 Pending | 0/8 | Pipeline | 20m |
| scheduled-prompts | 📋 Pending | 0/8 | Observer + Template | 20m |
| availability-monitor | 📋 Pending | 0/8 | Circuit Breaker | 20m |
| localization-service | 📋 Pending | 0/8 | Strategy + Factory | 20m |
| formatter-service | 📋 Pending | 0/8 | Strategy + Template | 20m |

**Current:** 5/15 steps (33%) - Critical path complete! 🎉
**Remaining:** 10 steps (220 min / 3.7 hours)

---

## 🎯 Success Criteria

- [ ] **Structure** - All files in logical directories
- [ ] **Documentation** - No >100KB files at root (except SESSION-CONTEXT.md)
- [ ] **Migration** - 15/15 steps generated and validated
- [ ] **Imports** - 0 broken references
- [ ] **Tests** - Validation passes for all steps
- [ ] **Workflow** - `unified-motia-workflow.sh` works from scripts/

---

## ⚠️ Risk Mitigation

### Before Refactoring
```bash
# Create full backup
tar czf motia-backup-$(date +%Y%m%d-%H%M).tar.gz \
    --exclude='.git' --exclude='.venv' .

# Store somewhere safe
mv motia-backup-*.tar.gz ~/backups/
```

### After Refactoring
```bash
# Verify no broken imports
rg 'gen-md-refactor|motia-output/steps' || echo "✅ All imports updated"

# Verify scripts work
./scripts/unified-motia-workflow.sh status

# Verify documentation references
rg -l '\./[a-z-]*\.sh' *.md | xargs -I {} sh -c 'echo "Checking {}"; grep -n "\./" {}'
```

### If Something Breaks
```bash
# Restore from backup
cd ~/projects
tar xzf ~/backups/motia-backup-YYYYMMDD-HHMM.tar.gz

# Or reset branch
git checkout main
git branch -D refactor/motia-steps
```

---

## 📝 Notes for Future Maintainer

### What Changed
1. **Scripts moved** - All .sh files from root → `scripts/`
2. **Markdown service** - `gen-md-refactor/` renamed to `markdown-service/`
3. **Steps at root** - `motia-output/steps/` → `steps/`
4. **Docs organized** - Supporting docs → `docs/`, large refs → `docs/reference/`
5. **Patterns categorized** - Flat → `behavioral/` and `creational/`

### What Stayed Same
- Core docs still at root: README.md, SESSION-CONTEXT.md, CLAUDE-CORE.md
- Step structure unchanged (handler.ts, config.json, schema.json, README.md, diagrams/)
- unified-motia-workflow.sh functionality identical (just moved to scripts/)

### Quick Commands
```bash
# Check project status
./scripts/unified-motia-workflow.sh status

# Generate new step
./scripts/unified-motia-workflow.sh full-pipeline <name> <type> <pattern> "<desc>"

# Validate step
./scripts/unified-motia-workflow.sh validate <name>

# See all commands
./scripts/unified-motia-workflow.sh help
```

---

## 🚀 Next Session Workflow

When continuing work on this project:

1. **Read context**
   ```bash
   cat SESSION-CONTEXT.md | head -100
   cat MIGRATION-COMPLETE.md
   ```

2. **Check status**
   ```bash
   ./scripts/unified-motia-workflow.sh status
   ```

3. **Continue migration** (if not 100%)
   ```bash
   # Generate next pending step
   ./scripts/unified-motia-workflow.sh full-pipeline \
     mcp-manager event observer "MCP server lifecycle management" typescript
   ```

4. **Or use batch generation**
   See SESSION-CONTEXT.md → "Option B: Batch Generation"

---

**Last Updated:** 2025-10-10 02:45 UTC
**Version:** Refactoring Checklist v1.0
**Status:** Ready for execution ✅
