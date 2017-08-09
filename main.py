import requests
import json
import datetime
import math

r = requests.get("http://www.nosdeputes.fr/deputes/enmandat/json", stream=True)
deputes = json.loads(r.text)

hemicycle = []

# Init of data
for depute in deputes["deputes"]:
    dep = {}
    dep['id'] = depute['depute']['id']
    dep['twitter'] = depute['depute']['twitter'] if len(depute['depute']['twitter']) > 0 else None
    dep['anciens_autres_mandats'] = depute['depute']['anciens_autres_mandats']
    dep['nom_circo'] = depute['depute']['nom_circo']
    dep['nom'] = depute['depute']['nom']
    dep['sexe'] = depute['depute']['sexe']
    dep['collaborateurs'] = depute['depute']['collaborateurs']
    dep['mandat_debut'] = depute['depute']['mandat_debut']
    dep['num_deptmt'] = depute['depute']['num_deptmt']
    dep['groupe_sigle'] = depute['depute']['groupe_sigle']
    dep['url_nosdeputes'] = depute['depute']['url_nosdeputes']
    hemicycle.append(dep)

now = datetime.datetime.now()

if now.month - 1 >= 10:
    r = requests.get("http://www.nosdeputes.fr/synthese/" + str(now.year) + str(now.month - 1) + "/json", stream=True)
else :
    r = requests.get("http://www.nosdeputes.fr/synthese/" + str(now.year) + "0" + str(now.month - 1) + "/json", stream=True)

synthese = json.loads(r.text)

total_amendements_adoptes = 0
total_amendements_proposes = 0
total_amendements_signes = 0
total_commission_interventions = 0
total_commission_presences = 0
total_hemicycle_interventions = 0
total_hemicycle_interventions_courtes = 0
total_propositions_ecrites = 0
total_propositions_signees = 0
total_questions_ecrites = 0
total_questions_orales = 0
total_rapports = 0
total_semaine = 0


# Get activity synthesis
for s_depute in synthese["deputes"]:
    for depute in hemicycle:
        if depute['id'] == s_depute['depute']['id']:
            depute['amendements_adoptes'] = s_depute['depute']['amendements_adoptes']
            depute['amendements_proposes'] = s_depute['depute']['amendements_proposes']
            depute['amendements_signes'] = s_depute['depute']['amendements_signes']
            depute['commission_interventions'] = s_depute['depute']['commission_interventions']
            depute['commission_presences'] = s_depute['depute']['commission_presences']
            depute['hemicycle_interventions'] = s_depute['depute']['hemicycle_interventions']
            depute['hemicycle_interventions_courtes'] = s_depute['depute']['hemicycle_interventions_courtes']
            depute['propositions_ecrites'] = s_depute['depute']['propositions_ecrites']
            depute['propositions_signees'] = s_depute['depute']['propositions_signees']
            depute['questions_ecrites'] = s_depute['depute']['questions_ecrites']
            depute['questions_orales'] = s_depute['depute']['questions_orales']
            depute['rapports'] = s_depute['depute']['rapports']
            depute['semaines_presence'] = s_depute['depute']['semaines_presence']
            total_amendements_adoptes = total_amendements_adoptes + depute['amendements_adoptes']
            total_amendements_proposes = total_amendements_proposes + depute['amendements_proposes']
            total_amendements_signes = total_amendements_signes + depute['amendements_signes']
            total_commission_interventions = total_commission_interventions + depute['commission_interventions']
            total_commission_presences = total_commission_presences + depute['commission_presences']
            total_hemicycle_interventions = total_hemicycle_interventions + depute['commission_interventions']
            total_hemicycle_interventions_courtes = total_hemicycle_interventions_courtes + depute['hemicycle_interventions_courtes']
            total_propositions_ecrites = total_propositions_ecrites + depute['propositions_ecrites']
            total_propositions_signees = total_propositions_signees + depute['propositions_signees']
            total_questions_ecrites = total_questions_ecrites + depute['questions_ecrites']
            total_questions_orales = total_questions_orales + depute['questions_orales']
            total_rapports =  total_rapports + depute['rapports']
            total_semaine = total_semaine + depute['semaines_presence']


partis = {}
for depute in hemicycle:
    if depute['groupe_sigle'] in partis.keys():
        partis[depute['groupe_sigle']].append(depute['id'])
    else:
        partis[depute['groupe_sigle']] = [];
        partis[depute['groupe_sigle']].append(depute['id'])

for parti in partis:
    print(parti + ":" + str(len(partis[parti])))


moy_amendements_adoptes = total_amendements_adoptes / len(hemicycle)
moy_amendements_proposes = total_amendements_proposes / len(hemicycle)
moy_amendements_signes = total_amendements_signes / len(hemicycle)
moy_commission_interventions = total_commission_interventions / len(hemicycle)
moy_commission_presences = total_commission_presences / len(hemicycle)
moy_hemicycle_interventions = total_hemicycle_interventions / len(hemicycle)
moy_hemicycle_interventions_courtes = total_hemicycle_interventions_courtes / len(hemicycle)
moy_propositions_ecrites = total_propositions_ecrites / len(hemicycle)
moy_propositions_signees = total_propositions_signees / len(hemicycle)
moy_questions_ecrites = total_questions_ecrites / len(hemicycle)
moy_questions_orales = total_questions_orales / len(hemicycle)
moy_rapports = total_rapports / len(hemicycle)
moy_semaine = total_semaine / len(hemicycle)

print(moy_semaine)

partis_pas_assidu = {}
partis_assidu = {}

# Stat Loop
# print(partis.keys())
# print(depute['groupe_sigle'] in partis.keys())
for depute in hemicycle:
    if depute['semaines_presence'] + 0.0 < moy_semaine:
        print("Le député(é) " + depute['nom'] + "du groupe " + depute["groupe_sigle"] + " n'est pas très assidu, ses présences relevé : " + str(depute['semaines_presence']) + " sont inférieurs à la moyenne de l'hémicycle.")
        if depute['groupe_sigle'] in partis_pas_assidu.keys():
            partis_pas_assidu[depute['groupe_sigle']].append(depute['id'])
        else:
            partis_pas_assidu[depute['groupe_sigle']] = [];
            partis_pas_assidu[depute['groupe_sigle']].append(depute['id'])

    else:
        print("Le député(é) " + depute['nom'] + "du groupe " + depute["groupe_sigle"] + " est assidu, ses présences relevé : " + str(depute['semaines_presence']) + " sont supérieurs à la moyenne de l'hémicycle.")
        if depute['groupe_sigle'] in partis_assidu.keys():
            partis_assidu[depute['groupe_sigle']].append(depute['id'])
        else:
            partis_assidu[depute['groupe_sigle']] = [];
            partis_assidu[depute['groupe_sigle']].append(depute['id'])

for parti in partis_pas_assidu:
    moy_pas_assidu = (len(partis_pas_assidu[parti]) + 0.0) / (len(partis[parti]) + 0.0)
    print("Le parti " + parti + " est composé de " + str(math.ceil(moy_pas_assidu * 100)) + " % de personnes en dilétente.")

for parti in partis_assidu:
    moy_assidu = (len(partis_assidu[parti]) + 0.0) / (len(partis[parti]) + 0.0)
    print("Le parti " + parti + " est composé de " + str(math.ceil(moy_assidu * 100)) + " % de personnes au taquet.")
