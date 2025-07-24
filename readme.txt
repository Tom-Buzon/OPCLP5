█████████████████████████████████████████████████████████████████████████████████
README - ARCHITECTURE DU PROJET MLOps | FUTURISYS P5
█████████████████████████████████████████████████████████████████████████████████

Ce projet vise à déployer un modèle de machine learning de manière professionnelle,
modulaire et reproductible, en séparant les environnements (démonstration, développement, production(equivalent a dev ici car on a pas de serveur de prod, mais l'idée est la il manquerait juste à switch))
tout en tirant parti de la plateforme Hugging Face pour la gestion centralisée du modèle.

──────────────────────────────────────────────────────────────
📁 STRUCTURE DES BRANCHES GIT
──────────────────────────────────────────────────────────────

🔸 `model`
   - ➕ Objectif : héberger une version démonstrative et stable du modèle
   - 🚀 Déploiement automatique sur **Hugging Face Spaces**
   - 📦 Contenu :
     - `model.joblib`, `te_encoder.joblib`, etc.
     - Un FastAPI léger ou Streamlit montrant l’usage du modèle
     - Un `requirements.txt` minimal
     - Pas de base de données ni de persistance

   ✅ Sert de vitrine publique ou démonstrateur
   ✅ Point d’entrée pour tester rapidement le modèle
   ✅ Code figé (tags : `model-v1.0.0`, `model-v1.0.2`, etc.)

──────────────────────────────────────────────────────────────

🔸 `dev`
   - ➕ Objectif : développement local avec interactions complètes
   - 🧠 Contenu :
     - FastAPI **connectée à une base PostgreSQL locale**
     - Connexion automatique au modèle hébergé via `hf_hub_download()`
     - Utilisation de SQLAlchemy pour gérer les prédictions en base
     - Tests automatisés (Pytest)
     - Variables d’environnement (.env)

   ✅ Environnement de test complet
   ✅ Permet le développement des features réelles
   ✅ Pipelines CI actifs (tests, qualité, formatage)

──────────────────────────────────────────────────────────────

🔸 `prod`
   - ➕ Objectif : version stable et validée du projet
   - 🎯 Contenu identique à `dev`, mais **consolidé, testé, approuvé**
   - 🔒 Pas de dev direct ici : on merge depuis `dev` uniquement
   - 🏷️ Tags Git (`v1.0.2`, `v1.0.3`) pour versionner les releases

   ✅ Source de vérité finale
   ✅ Peut être conteneurisé, déployé, mis en production

──────────────────────────────────────────────────────────────
⚙️ COMPORTEMENT PRÉVU PAR BRANCHE
──────────────────────────────────────────────────────────────

BRANCHE     | STREAMLIT        | FASTAPI           | DB           | MODÈLE
------------|------------------|-------------------|--------------|---------------------
model       | oui (simple)     | non (ou minimal)  | ❌           | local dans repo HF
dev         | oui (fonctionnel)| oui               | ✅ local     | téléchargé depuis HF
prod        | oui (prod ready) | oui               | ✅ local     | téléchargé depuis HF

──────────────────────────────────────────────────────────────
🎯 OBJECTIF MLOps
──────────────────────────────────────────────────────────────

Cette structure permet :
- Un déploiement continu clair par environnement
- Un historique de modèle versionné 
- Un découplage fort entre **model**, **dev**
- Une architecture modulaire, adaptée aux projets ML modernes

──────────────────────────────────────────────────────────────
🔗 UTILISATION DES BRANCHES
──────────────────────────────────────────────────────────────

🧱 Création de features :
> `feature/NomFeature` → merge dans `dev` après validation/test

📦 Push de modèle :
> `model` → push vers HF avec tag `model-vX.X.X`

🧪 Intégration continue :
> GitHub Actions : lint + tests unitaires sur chaque push dans `dev`

🚀 Livraison :
> `dev` → merge dans `prod` après QA
> `prod` → tag `vX.X.X`

──────────────────────────────────────────────────────────────
🧭 RECOMMANDATIONS
──────────────────────────────────────────────────────────────

- Garder une structure de dossier cohérente dans toutes les branches
- Isoler les fonctions communes (`model_utils.py`, `preprocessing.py`) dans `common/`
- Documenter chaque étape dans le `CHANGELOG.md`
- Utiliser `.env.example` pour faciliter la configuration

──────────────────────────────────────────────────────────────

🤝 Auteur : qneaub 
🎓 Projet : P5 | OpenClassrooms  
📅 Dernière mise à jour : 2025-07-24