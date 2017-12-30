from Fenetre import *
from Classes import *
import unittest
import os
from tkinter import *
class TestRenomTom(unittest.TestCase):
	"""docstring for TestRenomTom"""
	
	def testsFenetre(self):
		self.fenetre = Fenetre()
		self.assertTrue(self.fenetre.createMenu())
		self.assertTrue(self.fenetre.fenetreCreerRegle())
		self.assertTrue(self.fenetre.creerFormulaireRegle())
		self.assertTrue(self.fenetre.previsualisation())
		self.assertTrue(self.fenetre.fenetreListerRegle())
		self.assertTrue(self.fenetre.clearScreen())
		self.assertTrue(self.fenetre.fenetreRenommerRepertoire())
		self.assertTrue(self.fenetre.selectBoutonNouveauNom(None))

		self.fenetre.fenetreCreerRegle()
		self.fenetre.amorce.selection_clear(0)
		self.fenetre.amorce.select_set(1)
		self.fenetre.aPartirDe.insert(0, "A")
		self.fenetre.prefixe.insert(0, "--")
		self.fenetre.boutonNomOriginal.deselect()
		self.fenetre.boutonNouveauNom.select()
		self.fenetre.nomFichier.insert(0, "texte")
		self.fenetre.suffixe.insert(0, "--")
		self.fenetre.extension.insert(0, ".txt,.jpg")
		self.assertFalse(self.fenetre.traitementCreer())

		self.fenetre.fenetreRenommerRepertoire()
		self.fenetre.amorce.selection_clear(0)
		self.fenetre.amorce.select_set(1)
		self.fenetre.aPartirDe.insert(0, "A")
		self.fenetre.prefixe.insert(0, "--")
		self.fenetre.boutonNomOriginal.deselect()
		self.fenetre.boutonNouveauNom.select()
		self.fenetre.nomFichier.insert(0, "texte")
		self.fenetre.suffixe.insert(0, "--")
		self.fenetre.extension.insert(0, ".txt,.jpg")

		self.assertFalse(self.fenetre.traitementRenommer())
		self.assertTrue(self.fenetre.traitementListerSupprimer(Regle("Regless test","lettre","AB","_pre_","True","test","_suf_",".txt")))

	def TestsListeRegle(self):
		pass

os.system("cls")
unittest.main()