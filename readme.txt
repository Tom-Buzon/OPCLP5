█████████████████████████████████████████████████████████████████████████████████
README - ARCHITECTURE DU PROJET MLOps | FUTURISYS P5
█████████████████████████████████████████████████████████████████████████████████

Ce projet vise à déployer un modèle de machine learning de manière professionnelle,
modulaire et reproductible, en séparant les environnements (démonstration, développement, production(equivalent a dev ici car on a pas de serveur de prod, mais l'idée est la il manquerait juste à switch))
tout en tirant parti de la plateforme Hugging Face pour la gestion centralisée du modèle.

──────────────────────────────────────────────────────────────
🐧🍵 LANCEMENT DU PROJET
──────────────────────────────────────────────────────────────

YOU NEED A .ENV With a HF_TOKEN=xx_xxxxxxxxxxxxxxxxxxxxxx

poetry env activate 
uvicorn App.API.main:app --reload 


&

poetry env activate 
streamlit run App/streamlit_app_FastApi.py 

──────────────────────────────────────────────────────────────
📁 STRUCTURE DES BRANCHES GIT
──────────────────────────────────────────────────────────────

🔸 `model`     dispo online :https://huggingface.co/spaces/qneaup/opclp5
   - ➕ Objectif : héberger une version démonstrative et stable du modèle
   - 🚀 Déploiement automatique sur **Hugging Face Spaces**
   - 📦 Contenu :
     - `model.joblib`, `te_encoder.joblib`, etc.
     - Un FastAPI léger ou Streamlit montrant l’usage du modèle
     - Un `requirements.txt` minimal
     - Pas de base de données ni de persistance

   ✅ Sert de vitrine publique ou démonstrateur
   ✅ Point d’entrée pour tester rapidement le modèle
   ✅ Code figé (tags : `model-v1.0.0`)

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

lien HF(app dispo online):
https://huggingface.co/spaces/qneaup/opclp5

🧪 Intégration continue :
> GitHub Actions :  tests unitaires sur chaque push dans `dev`

🚀 Livraison :
> `dev` → merge dans `prod` après QA
> `prod` → tag `vX.X.X` → si on avait un server, on aurait une nouvelle serie de test GitAction au push. 


──────────────────────────────────────────────────────────────

🤝 Auteur : qneaub 
🎓 Projet : P5 | OpenClassrooms  
📅 Dernière mise à jour : 2025-07-24


devnotes:
etapese suivante :

-ajouter des test pytest sur dev pour toute les fonctions existante  👌🎉

-branche : feature/BigData                                       👌🎉
-ajouter une dblocal (utiliser SQL Alchemy + Postgres)               👌🎉
-connecter la db a l'FastAPI                                         👌🎉
-Ajouter des endpoint db FastAPI dans main.py                        👌🎉
-générer les doc automatiques                                        😶‍🌫️🫣

-générer un csv de X_test
-push le csv dans la base


-branche : feature/finalTouch
-corriger les endpoint sur des vrai data / vérification de la logique
-Mettre a jour laffichage streamlit : ou bien on selectionne un employé de la db, ou bien on applique la selection  || liste a checkbox et on repond un tableau ? 
-Verifier quon a bien tous les endpoints et test_

