import streamlit as st
import pandas as pd
import numpy as np
from utils import *
from datetime import datetime
import sys
import pickle
import re
import plotly.express as px
import matplotlib.pyplot as plt # Plotting library



def main():
    st.image("digital.jpg",width = 525)
    st.title('Recupération des actes de care')
    st.markdown(
    """
    Selectionner le ou les fichiers à importer
    """
    )


    data = []
    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        #st.write("filename:", uploaded_file.name)
        data.append(bytes_data)



        data1 = data[0]
        data2 = data[1]
        data3 = data[2]
        _Avec = data1.iloc[:,[0,4]]
        _Temp = data2.iloc[:,:]
        _Hors = data3.iloc[:,[0,5]]

        st.write("",_Hors.head())

        

        # 1. Récuperation code puk

        pukA = ["PUK_dashboard","PUK_sidemenu","PUK_display_success","code_puk_launch","code_puk_success"]
        pukH = ["Récupérer code PUK | Orange Côte d’Ivoire"]
        _A1 = [_Avec[_Avec["Page Title"]==i].loc[:,"Users"] for i in pukA][0].sum()+[_Avec[_Avec["Page Title"]==i].loc[:,"Users"] for i in pukA][1].sum()+[_Avec[_Avec["Page Title"]==i].loc[:,"Users"] for i in pukA][2].sum()+[_Avec[_Avec["Page Title"]==i].loc[:,"Users"] for i in pukA][3].sum()+[_Avec[_Avec["Page Title"]==i].loc[:,"Users"] for i in pukA][4].sum()
        _H1 = [_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in pukH][0].sum()
        RecupPuk = _A1+_H1
        print("Récup puk:{}".format(RecupPuk))

        # 2. Consultation facture

        Consul_factA = ["ACE_FACTURE_weblink","ACE_facture_dashboard","ACE_FACTURE_dashboard"]
        Consul_factH = ["ACE_FACTURE_weblink","ACE_facture_dashboard","ACE_FACTURE_dashboard","Payer Factures | Mon espace Orange et Moi"]
        _A2 = [_Avec[_Avec["Page Title"]==i].loc[:,"Users"] for i in Consul_factA][1].sum()+[_Avec[_Avec["Page Title"]==i].loc[:,"Users"] for i in Consul_factA][2].sum()
        _H2 = [_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in Consul_factH][0].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in Consul_factH][1].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in Consul_factH][2].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in Consul_factH][3].sum()
        Consfact = _A2+_H2

        # 3. Consultation solde

        ConsSoldA = ["MyBalance_dashboard","MyBalance_icon"]
        ConsSoldH = ["MyBalance_dashboard","MyBalance_icon"]
        _A3 = [_Avec[_Avec["Page Title"]==i].loc[:,"Users"] for i in ConsSoldA][0].sum()+[_Avec[_Avec["Page Title"]==i].loc[:,"Users"] for i in ConsSoldA][1].sum()
        _H3 = [_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in ConsSoldH][0].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in ConsSoldH][1].sum()
        ConsSold = _A3+_H3

        # 4. Désabonnement SVA

        DesabSVA = ["ShareData_DesactivationService_Success"]

        _A4 = [_Avec[_Avec["Page Title"]==i].loc[:,"Users"] for i in DesabSVA][0].sum()
        DsabSVA = _A4

        # 5. User Guide

        guidB2B = ["mon espace client | corporate b2b"]
        _A5 = [_Temp[_Temp["Event Category"]==i].loc[:,'Total Events'] for i in guidB2B][0].sum()
        gdB2B = _A5

        # 6. Télécharger facture

        telecharger = ["télécharger ma facture"]
        _A6 = [_Temp[_Temp["Event Label"]==i].loc[:,"Total Events"] for i in telecharger][0].sum()
        téléch = _A6
        print("téléfact:{}".format(téléch))


        # 7. Déblocage Compte OM

        deblo = ["Comment débloquer mon compte Orange Money ? | Orange Côte d’Ivoire","(1) Comment débloquer mon compte Orange Money ? | Orange Côte d’Ivoire"]
        _H7 = [_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in deblo][0].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in deblo][1].sum()
        _deblo = _H7

        # 8. Dépot reclamation

        recla = ["Reclamation | Corporate B2b","Formulaire Reclamation | Orange Côte d’Ivoire","Réclamation en ligne | Orange Côte d’Ivoire"]
        _H8 = [_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in recla][0].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in recla][1].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in recla][2].sum()
        _recla = _H8

        # 9. Deplafonnement compte OM

        deplaf = ["assistance déplafonner mon compte Orange Money | Orange Côte d’Ivoire"]
        _H9 = [_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in deplaf][0].sum()
        _deplaf = _H9

        # 10. Historique de transaction

        h_de_tran = ["Détails historique | Mon espace Orange et Moi","Détails historique |"]
        _H10 = [_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in h_de_tran][0].sum()
        _histTr = _H10

        # 11. Historique B2B

        h_b2b = ["Historique de rechargement | Corporate B2b"]
        _H11 = [_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in h_b2b][0].sum()
        _histB = _H11

        # 12. Suivi Conso

        suivCon =["Suivi Conso | Mon espace Orange et Moi","Suivi Conso |","Suivi conso | Mon espace Orange et Moi","Suivi conso |"]
        _H12 = [_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in suivCon][0].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in suivCon][1].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in suivCon][2].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in suivCon][3].sum()
        _svCons = _H12

        # 13. Configuration

        conf = ["Configuration du compte Internet (ADSL) | Orange Côte d’Ivoire","configuration du routeur fibre ZTE ZXHN F660 | Orange Côte d’Ivoire","Mobile configuration | Orange Ivory Coast","ZTE ZXHN F660 fiber router configuration | Orange Ivory Coast","Configuration mobile | Orange Côte d’Ivoire","Accédez à l''interface de configuration de la Livebox 2. | Orange Côte d’Ivoire"]
        _H13 = [_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in conf][0].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in conf][1].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in conf][2].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in conf][3].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in conf][4].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in conf][5].sum()
        _config = _H13

        # 14. Creation Compte

        cr_cpt_OM = ["Créez un compte Orange Money |","Comment créer mon compte | Orange Côte d’Ivoire","assistance ouvrir compte orange money | Orange Côte d’Ivoire","(1) Assistance ouvrir un compte orange money | Orange Côte d’Ivoire","(2) Assistance ouvrir un compte orange money | Orange Côte d’Ivoire","Assistance ouvrir un compte orange money | Orange Côte d’Ivoire"]
        _H14 = [_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in cr_cpt_OM][0].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in cr_cpt_OM][1].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in cr_cpt_OM][2].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in cr_cpt_OM][3].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in cr_cpt_OM][4].sum()+[_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in cr_cpt_OM][5].sum()
        _CrcptOM = _H14
        print("Suivi conso: {}".format(_CrcptOM))


        # 15. Code utile

        code_util = ["Mes codes pratiques Orange money | Orange Côte d’Ivoire"]

        _H15 = [_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in code_util][0].sum()
        _Cd_util = _H15

        #16. Restauration 

        restau = ["(1) assistance sauvegarde de repertoire | Orange Côte d’Ivoire","assistance sauvegarde de repertoire | Orange Côte d’Ivoire"]


        _H16 = [_Hors[_Hors["Page Title"]==i].loc[:,"Users"] for i in restau][1].sum()
        _rest = _H16

        _Final = pd.DataFrame({"Acte de care":["RécupPuk","CsulFact","DsabSVA","UsGuidB2B","TélFact","DblocptOM","DpoRécla","DplafcptOM","HistTrans","HistTrB2B","SuivConso","Config","Créacpt","CodUtil","Restau"],
                            "Volume":[RecupPuk,Consfact,DsabSVA,gdB2B,téléch,_deblo,_recla,_deplaf,_histTr,_histB,_svCons,_config,_CrcptOM,_Cd_util,_rest]})


        _Final.iloc[:,1].sum()


        Donnees = _Final.sort_values(by="Volume",ascending = False)

        st.write("",Donnees)


if __name__ == '__main__':
    main()

