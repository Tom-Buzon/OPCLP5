

🧠 **TechNova Partners – Analyse de Turnover**

Ce projet vise à comprendre les facteurs expliquant le départ des salariés chez TechNova Partners, à l’aide d’une analyse exploratoire détaillée, d’une modélisation prédictive et d’une interprétation locale et globale des décisions.


🔧 Environnement

Le projet utilise Python 3.10 (nécessaire pour la compatibilité avec SHAP).
Un environnement virtuel peut être configuré avec Poetry 
💡 L’environnement est optionnel, car la majorité des dépendances sont classiques (Pandas, XGBoost, etc.).


📁 Structure du projet

    📁  buzon_tom_notebook_OLD.ipynb

Analyse exploratoire complète :
-Étude par variable (catégorielle, continue, ordinale),
-Visualisations détaillées,
-Comparaison de plusieurs modèles de classification avec différents scores de validation.

    📁  buzon_tom_notebook_VF.ipynb

Version optimisée pour la soutenance :
-Pipeline de preprocessing,
-Entraînement du meilleur modèle (XGBoost),
-Interprétation avec SHAP (feature importance locale et globale),
-Préparation des résultats finaux pour la présentation.

    📁  buzon_tom_notebook_merge_des_tables.ipynb

Logique métier de fusion des trois fichiers Excel fournis par l’entreprise :
-Jointure cohérente par ID,
-Validation de l’intégrité des données.

    📊  Présentation final : buzon_tom_presentation_TechNova_Parteners.pptx

Présentation PowerPoint 15 minutes :
-Résumé de l’étude,
-Insights clés,
-Méthodologie de modélisation,
/Résultats interprétables et recommandations RH.



✅ Résultat
Le modèle final :

Permet d’identifier les profils à haut risque de départ,
S’appuie sur des variables clés validées par SHAP et les scores de gain,
Fournit des recommandations RH concrètes basées sur l’analyse.



Made with ❤️ by qneaub.