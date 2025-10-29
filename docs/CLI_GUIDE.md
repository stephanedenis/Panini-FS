# Panini-FS CLI Guide

Complete command-line interface for Panini-FS v2.0

---

## Installation

```bash
cargo install --path crates/panini-cli
```

Or build from source:
```bash
cd crates/panini-cli
cargo build --release
./target/release/panini-cli --version
```

---

## Quick Start

```bash
# Initialize new repository
panini-cli init my-knowledge-base
cd my-knowledge-base

# Create your first concept
panini-cli create quantum_physics \
  --title "Quantum Physics" \
  --tags "physics,science" \
  --dhatu SEEKING

# Read it back
panini-cli read quantum_physics

# List all concepts
panini-cli list
```

---

## Commands

### `init` - Initialize Repository

Create a new Panini-FS repository.

**Usage:**
```bash
panini-cli init [PATH]
```

**Arguments:**
- `PATH` (optional) - Repository path (default: current directory)

**Examples:**
```bash
# Initialize in current directory
panini-cli init

# Initialize in specific path
panini-cli init ~/my-knowledge-base

# Initialize with absolute path
panini-cli init /home/user/projects/knowledge
```

**Output:**
```
✅ Repository initialized: /home/user/my-knowledge-base
```

---

### `create` - Create Concept

Create a new concept in the repository.

**Usage:**
```bash
panini-cli create <ID> --title <TITLE> [OPTIONS]
```

**Arguments:**
- `ID` (required) - Unique concept identifier (lowercase, underscores allowed)
- `--title <TITLE>` (required) - Human-readable title

**Options:**
- `--tags <TAGS>` - Comma-separated tags
- `--dhatu <TYPE>` - Emotional dhatu type

**Dhatu Types:**
- `SEEKING` - Exploration, curiosity
- `RAGE` - Anger, frustration
- `FEAR` - Anxiety, threat
- `LUST` - Desire, attraction
- `CARE` - Nurturing, protection
- `PANIC` - Separation distress
- `PLAY` - Joy, playfulness

**Examples:**
```bash
# Simple concept
panini-cli create neuroscience --title "Neuroscience"

# With tags
panini-cli create machine_learning \
  --title "Machine Learning" \
  --tags "ai,data-science,ml"

# With dhatu
panini-cli create meditation \
  --title "Meditation Practice" \
  --dhatu CARE

# Complete concept
panini-cli create quantum_computing \
  --title "Quantum Computing" \
  --tags "physics,computing,quantum" \
  --dhatu SEEKING
```

**Output:**
```
✅ Created: quantum_computing
```

---

### `read` - Read Concept

Display concept details.

**Usage:**
```bash
panini-cli read <ID> [--json]
```

**Arguments:**
- `ID` (required) - Concept identifier

**Options:**
- `--json` - Output as JSON

**Examples:**
```bash
# Human-readable format
panini-cli read quantum_computing

# JSON format
panini-cli read quantum_computing --json
```

**Output (human-readable):**
```
📄 Concept: quantum_computing
Title: Quantum Computing
Dhatu: SEEKING
Tags: physics, computing, quantum
Created: 2025-01-15 10:30:00 UTC
```

**Output (JSON):**
```json
{
  "id": "quantum_computing",
  "title": "Quantum Computing",
  "dhatu": "SEEKING",
  "tags": ["physics", "computing", "quantum"],
  "created_at": "2025-01-15T10:30:00Z"
}
```

---

### `update` - Update Concept

Modify existing concept.

**Usage:**
```bash
panini-cli update <ID> [OPTIONS]
```

**Arguments:**
- `ID` (required) - Concept identifier

**Options:**
- `--title <TITLE>` - New title
- `--tags <TAGS>` - New tags (replaces existing)

**Examples:**
```bash
# Update title only
panini-cli update quantum_computing \
  --title "Quantum Computing Fundamentals"

# Update tags only
panini-cli update quantum_computing \
  --tags "physics,computing,quantum,qubits"

# Update both
panini-cli update quantum_computing \
  --title "Quantum Computing: Theory & Practice" \
  --tags "quantum,theory,practice"
```

**Output:**
```
✅ Updated: quantum_computing
```

---

### `delete` - Delete Concept

Remove concept from repository.

**Usage:**
```bash
panini-cli delete <ID>
```

**Arguments:**
- `ID` (required) - Concept identifier

**Examples:**
```bash
panini-cli delete old_concept
```

**Output:**
```
✅ Deleted: old_concept
```

**Warning:** This operation is permanent (unless you use Git history).

---

### `list` - List Concepts

Show all concepts in repository.

**Usage:**
```bash
panini-cli list [--json]
```

**Options:**
- `--json` - Output as JSON array

**Examples:**
```bash
# Human-readable list
panini-cli list

# JSON array
panini-cli list --json
```

**Output (human-readable):**
```
📚 Concepts (5):
  - quantum_computing
  - machine_learning
  - neuroscience
  - meditation
  - philosophy
```

**Output (JSON):**
```json
[
  "quantum_computing",
  "machine_learning",
  "neuroscience",
  "meditation",
  "philosophy"
]
```

---

### `add-relation` - Add Relation

Create relation between concepts.

**Usage:**
```bash
panini-cli add-relation <SOURCE> --rel-type <TYPE> <TARGET> [--confidence <0-1>]
```

**Arguments:**
- `SOURCE` (required) - Source concept ID
- `--rel-type <TYPE>` (required) - Relation type
- `TARGET` (required) - Target concept ID
- `--confidence <SCORE>` (optional) - Confidence 0-1 (default: 1.0)

**Relation Types:**
- `is_a` - Taxonomic hierarchy (dog is_a animal)
- `part_of` - Composition (wheel part_of car)
- `causes` - Causation (heat causes expansion)
- `contradicts` - Opposition (hot contradicts cold)
- `supports` - Support (evidence supports theory)
- `derives_from` - Derivation (equation derives_from axiom)
- `used_by` - Usage (hammer used_by carpenter)
- `related_to` - General association

**Examples:**
```bash
# Simple relation
panini-cli add-relation dog --rel-type is_a animal

# With confidence
panini-cli add-relation theory --rel-type supports hypothesis --confidence 0.85

# Compositional
panini-cli add-relation engine --rel-type part_of car

# Causal
panini-cli add-relation stress --rel-type causes anxiety --confidence 0.75

# Contradictory
panini-cli add-relation order --rel-type contradicts chaos
```

**Output:**
```
✅ Added relation: dog is_a animal
```

---

### `relations` - Get Relations

Show all relations for a concept.

**Usage:**
```bash
panini-cli relations <ID>
```

**Arguments:**
- `ID` (required) - Concept identifier

**Examples:**
```bash
panini-cli relations quantum_computing
```

**Output:**
```
🔗 Relations for quantum_computing:
  → is_a computing_paradigm (1.00)
  → part_of quantum_technology (1.00)
  → related_to quantum_physics (0.95)
  ← used_by quantum_algorithms (1.00)
```

**Legend:**
- `→` - Outgoing relation (this concept → other)
- `←` - Incoming relation (other → this concept)
- `(0.95)` - Confidence score

---

### `sync` - Synchronize

Sync repository with remote (Git pull + push).

**Usage:**
```bash
panini-cli sync
```

**No arguments.**

**Examples:**
```bash
panini-cli sync
```

**Output:**
```
⏳ Syncing with remote...
✅ Pull complete
✅ Push complete
✅ Sync successful
```

**Requirements:**
- Git remote configured
- Network connectivity
- Authentication (SSH/HTTPS)

---

### `status` - Repository Status

Show repository state and statistics.

**Usage:**
```bash
panini-cli status
```

**No arguments.**

**Examples:**
```bash
panini-cli status
```

**Output:**
```
📊 Repository Status:

Concepts: 42
Relations: 156
Uncommitted changes: 3
Last sync: 2025-01-15 14:30:00 UTC

Git Status:
  Modified: 2 files
  New: 1 file
```

---

## Workflow Examples

### Building a Knowledge Graph

```bash
# Initialize
panini-cli init my-knowledge

# Create taxonomy
panini-cli create animal --title "Animal" --dhatu SEEKING
panini-cli create mammal --title "Mammal" --dhatu SEEKING
panini-cli create dog --title "Dog" --dhatu CARE

# Build hierarchy
panini-cli add-relation mammal --rel-type is_a animal
panini-cli add-relation dog --rel-type is_a mammal

# View relations
panini-cli relations dog
# Output:
#   → is_a mammal (1.00)
#   → is_a animal (transitive, 1.00)
```

---

### Research Project

```bash
# Create research concepts
panini-cli create hypothesis_1 \
  --title "Neural Plasticity Hypothesis" \
  --tags "neuroscience,research" \
  --dhatu SEEKING

panini-cli create evidence_1 \
  --title "fMRI Study Results" \
  --tags "neuroscience,data" \
  --dhatu SEEKING

panini-cli create theory_neuroplasticity \
  --title "Neuroplasticity Theory" \
  --tags "neuroscience,theory" \
  --dhatu SEEKING

# Link evidence to hypothesis
panini-cli add-relation evidence_1 \
  --rel-type supports hypothesis_1 \
  --confidence 0.85

# Link hypothesis to theory
panini-cli add-relation hypothesis_1 \
  --rel-type derives_from theory_neuroplasticity

# Check relationships
panini-cli relations hypothesis_1
```

---

### Team Collaboration

```bash
# Alice creates concept
panini-cli create feature_x --title "Feature X Design"
panini-cli sync

# Bob pulls and adds details
panini-cli sync
panini-cli update feature_x --tags "frontend,ui,priority-high"

# Bob creates related concept
panini-cli create implementation_x --title "Feature X Implementation"
panini-cli add-relation implementation_x --rel-type derives_from feature_x
panini-cli sync

# Alice reviews
panini-cli sync
panini-cli read implementation_x
panini-cli relations implementation_x
```

---

## Configuration

### Environment Variables

```bash
# Repository path (if not using current directory)
export PANINI_REPO=/path/to/repo

# Git remote URL
git -C $PANINI_REPO remote add origin https://github.com/user/repo.git

# Git user config
git -C $PANINI_REPO config user.name "Your Name"
git -C $PANINI_REPO config user.email "your.email@example.com"
```

---

## Shell Completion

### Bash

```bash
panini-cli --generate-completion bash > ~/.config/panini-cli/completion.bash
echo 'source ~/.config/panini-cli/completion.bash' >> ~/.bashrc
```

### Zsh

```bash
panini-cli --generate-completion zsh > ~/.config/panini-cli/completion.zsh
echo 'source ~/.config/panini-cli/completion.zsh' >> ~/.zshrc
```

### Fish

```bash
panini-cli --generate-completion fish > ~/.config/fish/completions/panini-cli.fish
```

---

## Troubleshooting

### Command Not Found

```bash
# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Or use full path
~/.cargo/bin/panini-cli --version
```

### Repository Not Found

```bash
# Initialize first
panini-cli init

# Or specify path
panini-cli --repo-path /path/to/repo list
```

### Sync Failures

```bash
# Check Git remote
git remote -v

# Pull manually
git pull

# Resolve conflicts
git status
# Edit files, then:
git add .
git commit -m "Resolve conflicts"
git push
```

### Invalid Relation Type

Valid types: `is_a`, `part_of`, `causes`, `contradicts`, `supports`, `derives_from`, `used_by`, `related_to`

```bash
# Wrong
panini-cli add-relation a --rel-type belongs_to b
# Error: Invalid relation type

# Correct
panini-cli add-relation a --rel-type part_of b
```

---

## Tips & Best Practices

1. **Use meaningful IDs**: `quantum_entanglement` not `qe1`
2. **Tag consistently**: Establish tag taxonomy early
3. **Sync frequently**: Avoid conflicts with `panini-cli sync`
4. **Check relations**: Use `panini-cli relations <id>` to explore graph
5. **JSON for scripts**: Use `--json` for programmatic processing
6. **Git integration**: Leverage Git history for versioning

---

## Scripting Examples

### Bash: Batch Create

```bash
#!/bin/bash
# create_taxonomy.sh

concepts=(
  "animal:Animal"
  "mammal:Mammal"
  "reptile:Reptile"
  "bird:Bird"
)

for entry in "${concepts[@]}"; do
  IFS=':' read -r id title <<< "$entry"
  panini-cli create "$id" --title "$title" --dhatu SEEKING
done

panini-cli add-relation mammal --rel-type is_a animal
panini-cli add-relation reptile --rel-type is_a animal
panini-cli add-relation bird --rel-type is_a animal
```

### Python: Batch Import

```python
import subprocess
import json

concepts = [
    {"id": "ai", "title": "Artificial Intelligence", "tags": ["tech", "ai"]},
    {"id": "ml", "title": "Machine Learning", "tags": ["tech", "ai", "ml"]},
    {"id": "dl", "title": "Deep Learning", "tags": ["tech", "ai", "ml", "dl"]},
]

for concept in concepts:
    cmd = ["panini-cli", "create", concept["id"], "--title", concept["title"]]
    if "tags" in concept:
        cmd.extend(["--tags", ",".join(concept["tags"])])
    subprocess.run(cmd)

subprocess.run(["panini-cli", "add-relation", "ml", "--rel-type", "part_of", "ai"])
subprocess.run(["panini-cli", "add-relation", "dl", "--rel-type", "part_of", "ml"])
```

---

## Next Steps

- Read [API Documentation](API.md) for REST interface
- Explore [Architecture Guide](ARCHITECTURE.md) for system design
- Check [Git Integration](GIT_INTEGRATION.md) for versioning details
- See [Examples](examples/) for more use cases

---

**Version:** 2.0.0-alpha  
**Last Updated:** 2025-10-29
