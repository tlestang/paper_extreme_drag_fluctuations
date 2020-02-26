#!/bin/bash
#
### variables SGE
### shell du job
#$ -S /bin/bash
### nom du job (a changer)
#$ -N resimul_0
### file d'attente (a changer)
#$ -q monointeldeb48
### charger l'environnement utilisateur pour SGE
#$ -cwd
### exporter les variables d'environnement sur tous les noeuds d'execution
#$ -V

# aller dans le repertoire de travail/soumission
# important, sinon, le programme est lancé depuis ~/
cd ${SGE_O_WORKDIR}

source /usr/share/lmod/lmod/init/bash
module load Python/3.6.1

exec_line

# fin
