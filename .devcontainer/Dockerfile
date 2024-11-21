FROM texlive/texlive:latest

# Mettre à jour tlmgr et TeX Live
RUN tlmgr update --self && tlmgr update --all

# Installer uniquement les packages disponibles
RUN tlmgr install fontspec pgfplots

# Définir un répertoire de travail
WORKDIR /workspace

# Point d'entrée par défaut
CMD ["/bin/sh"]