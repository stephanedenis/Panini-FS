# 🎯 GUIDE VISUEL PAT GITHUB - Navigation Étape par Étape

## 📍 **VOUS ÊTES ICI** 
→ https://github.com/settings/tokens

## 🚀 **ÉTAPES DÉTAILLÉES**

### **1️⃣ Sur la page tokens (actuelle)**
```
✅ VOUS VOYEZ: "Personal access tokens"
✅ CHERCHEZ: Bouton vert "Generate new token"
✅ CLIQUEZ: "Generate new token" → Sélectionnez "Generate new token (classic)"
```

### **2️⃣ Page "New personal access token"**
```
📝 Note: PaniniFS-Development-Full
📅 Expiration: 90 days (ou "No expiration")
📋 Select scopes: VOIR CI-DESSOUS ⬇️
```

### **3️⃣ SCOPES À COCHER (dans l'ordre d'apparition)**

#### **🔴 OBLIGATOIRES (ERREUR si manquants)**
```
☑️ repo
   ☑️ repo:status
   ☑️ repo_deployment
   ☑️ public_repo
   ☑️ repo:invite
   ☑️ security_events

☑️ workflow

☑️ admin:org
   ☑️ write:org
   ☑️ read:org  ← ⚠️ CELUI-CI MANQUAIT ! Erreur corrigée

☑️ write:packages
   ☑️ read:packages

☑️ codespace  ← Pour GitHub Codespaces
```

#### **🟡 RECOMMANDÉS (utiles)**
```
☑️ gist
☑️ notifications
☑️ user
   ☑️ read:user
   ☑️ user:email
☑️ admin:public_key
   ☑️ read:public_key
   ☑️ write:public_key
```

### **4️⃣ Validation finale**
```
🔍 VÉRIFIEZ: "read:org" est bien coché
🟢 CLIQUEZ: "Generate token" (bouton vert en bas)
📋 COPIEZ: Le token généré (PAT GitHub)
```

## 🎯 **NAVIGATION ALTERNATIVE**

Si vous avez du mal à trouver, essayez cette navigation:

### **Route 1: Via Settings**
```
1. GitHub.com → Votre avatar (coin haut-droite)
2. Settings
3. Dans le menu gauche: "Developer settings" (tout en bas)
4. "Personal access tokens"
5. "Tokens (classic)"
6. "Generate new token"
```

### **Route 2: URL Directe**
```
https://github.com/settings/personal-access-tokens/new
```

## 🔧 **APRÈS GÉNÉRATION**

### **Test Immédiat**
```bash
# Dans votre terminal
gh auth logout
gh auth login

# Coller le nouveau token quand demandé
```

### **Validation**
```bash
gh auth status
# Doit afficher: "Logged in to github.com as stephanedenis (oauth_token)"
```

---

## 🆘 **SI TOUJOURS DIFFICILE**

Je peux vous aider en temps réel ! Dites-moi:
1. **Que voyez-vous** sur la page actuelle ?
2. **Quels boutons** sont visibles ?
3. **Quelle étape** vous bloque ?

La page devrait ressembler à une liste de vos tokens existants avec un bouton vert "Generate new token".

## 🎯 **OBJECTIF FINAL**
✅ PAT avec scope `read:org` → ✅ GitHub CLI fonctionnel → ✅ Autonomie cloud totale !
