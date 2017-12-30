from tkinter import *
from tkinter import filedialog
from Classes import *
import os
class Fenetre(Tk):
	"""
	Classe permettant de créer une fenètre de notre application. Cette classe s'occupe de toute la partie interfaces.
	"""
	def __init__(self):
		"""
		Constructeur configurant la fenètre suivant nos exigences : 
		- Impossible de la resize
		- Ajotu de la liste de règles
		- Ouverture de la fenètre lister règles.
		"""
		super(Fenetre, self).__init__()
		self.tk.call('wm', 'iconphoto', self, PhotoImage(file='RenomTomIcon.gif'))
		self.resizable(width=False, height=False)
		self.grid_columnconfigure(0, weight=2)
		self.grid_rowconfigure(0, weight=2)
		self.lesRegles = ListeRegle().charger()
		self.fenetreListerRegle()

	def fenetreCreerRegle(self):
		"""
		Méthode s'occupant de créer l'interface de la fenètre de création des règles.
		"""
		self.clearScreen()
		self.createMenu()
		self.title("RenomTom - Créer une règle")

		Label(self, text="Créer une règle", font=("Helvetica", 22)).grid(row=0, column=0, rowspan=1,  columnspan=7, pady=10)

		Label(self, text="Nom de la règle", font=("Helvetica", 16)).grid(row=3, column=2, rowspan=1,  columnspan=2)
		self.regle = Entry(self, font=("Helvetica", 14))
		self.regle.grid(row=3, column=4, pady=40, columnspan=2)
		self.creerFormulaireRegle()
		self.envoyer = Button(self, text="\n  Créer  \n", command=lambda :self.traitementCreer())
		self.envoyer.grid(sticky=N, row=8, column=6, rowspan=4,  columnspan=2, padx=20)
		return True

	def fenetreRenommerRepertoire(self):
		"""
		Méthode s'occupant de créer l'interface de la fenètre de renommage de répertoire.
		"""
		self.clearScreen()
		self.createMenu()
		self.title("RenomTom - Renommer un répertoire")
		
		self.icon = PhotoImage(file="RenomTomIcon.gif").subsample(7)
		self.canvasIcon = Canvas(self, width=50, height=80)
		self.canvasIcon.grid(sticky=N+W+S+E, row=1, column=6, rowspan=1,  columnspan=1)
		self.canvasIcon.create_image(50, 50, image=self.icon)

		Label(self, text="Renommer en lots", font=("Helvetica", 22)).grid(row=1, column=1, rowspan=1,  columnspan=6)

		Label(self, text="Nom du répertoire", font=("Helvetica", 16)).grid(row=3, column=2, rowspan=1,  columnspan=2)
		self.nomRepertoire = Entry(self, font=("Helvetica", 14), width=30)
		self.nomRepertoire.grid(sticky=E, row=3, column=4, pady=20, columnspan=2)

		self.browse = Button(self, text="\tParcourir\t", command=self.rechercher)
		self.browse.grid(sticky=W, row=3, column=6, pady=40, columnspan=2)

		self.creerFormulaireRegle()
		self.envoyer = Button(self, text="\n  Renommer  \n", command=self.traitementRenommer)
		self.envoyer.grid(sticky=N, row=8, column=6, rowspan=4,  columnspan=2, padx=20)
		return True

	def rechercher(self):
		"""
		Ouvre une boite de dialogue pour choisir un fichier
		"""
		self.nomRepertoire.insert(0, filedialog.askdirectory(initialdir =os.path.expanduser("~") + "\\Documents",title = "Choisissez un répertoire"))

	def creerFormulaireRegle(self):
		"""
		Méthode permettant de créer le formulaire des règles. Commun à deux fenètres :
		- Renommage de répertoire
		- Créer une règle
		"""
		Label(self, text="Amorce", font=("Helvetica", 13)).grid(row=6, column=1, padx=20)
		self.amorce = self.creerListe(["Aucune","Lettre","Chiffre"])
		self.amorce.grid(row=7, column=1, rowspan=2,  columnspan=1, padx=20)
		Label(self, text="À partir de", font=("Helvetica", 13)).grid(row=9, column=1, padx=20)
		self.aPartirDe = Entry(self, font=("Helvetica", 13))
		self.aPartirDe.grid(row=10, column=1, padx=20, pady=10)

		Label(self, text="Préfixe", font=("Helvetica", 13)).grid(row=6, column=2)
		self.prefixe = Entry(self, font=("Helvetica", 13))
		self.prefixe.grid(sticky=N, row=7, column=2)
		
		Label(self, text="Nom du fichier", font=("Helvetica", 13)).grid(row=6, column=3,  columnspan=2)
		self.checkRadio = IntVar()
		self.boutonNomOriginal = Radiobutton(self, text="Nom original", font=("Helvetica", 13), value=1, variable=self.checkRadio)
		self.boutonNomOriginal.grid(sticky=W+N, row=7, column=3, columnspan=2)
		self.boutonNouveauNom = Radiobutton(self, value=2, variable=self.checkRadio)
		self.boutonNouveauNom.grid(sticky=W+N, row=8, column=3)
		self.nomFichier = Entry(self, font=("Helvetica", 13), width=14)
		self.nomFichier.bind('<Button-1>', self.selectBoutonNouveauNom)
		self.nomFichier.grid(sticky=W+N, row=8, column=4)

		Label(self, text="Suffixe", font=("Helvetica", 13)).grid(row=6, column=5)
		self.suffixe = Entry(self, font=("Helvetica", 13))
		self.suffixe.grid(sticky=N, row=7, column=5)

		Label(self, text="Extensions concernées", font=("Helvetica", 13)).grid(row=6, column=6, padx=20)
		self.extension = Entry(self)
		self.extension.grid(sticky=N, row=7, column=6, padx=20)

		self.aPartirDe.bind("<KeyRelease>", self.previsualisation)
		self.prefixe.bind("<KeyRelease>", self.previsualisation)
		self.nomFichier.bind("<KeyRelease>", self.previsualisation)
		self.suffixe.bind("<KeyRelease>", self.previsualisation)
		self.extension.bind("<KeyRelease>", self.previsualisation)
		return True

	
	def previsualisation(self, e=None):
		"""
		S'occupe de la prévisualisation de la page. Le paramètre passé en paramètre n'est pas utile au bon fonctionnement.
		"""
		try:
			self.previ.grid_remove()
			self.previ.destroy()
		except Exception as e:
			pass
		self.previ = Label(self, font=("Helvetica", 11), text="Prévisualisation : " + self.aPartirDe.get() + self.prefixe.get() + self.nomFichier.get() + self.suffixe.get() + self.extension.get().split(",")[0])
		self.previ.grid(row=10, column=2,  columnspan=4)
		return True
	
	def fenetreListerRegle(self):
		"""
		Méthode s'occupant de créer l'interface de la fenètre permettant de lister les règles.
		On y retrouve un bouton 'Utiliser' qui redirige vers la page de renommage de répertoire et qui remplit les champs
		par les propriétées de la règle.
		On y trouve également un bouton 'Supprimer'. Celui-ci sert à supprimer la règle en question. Elle sera également supprimée du fichier de sauvegarde.
		"""
		self.clearScreen()
		self.createMenu()
		self.title("RenomTom - Liste des règles")

		Label(self, text="Toutes les règles", font=("Helvetica", 22)).grid(row=0, column=0, rowspan=1,  columnspan=8, pady=10)
		Label(self, text="Amorce", font=("Helvetica bold", 13)).grid(row=1, column=2, padx=10, pady=10)
		Label(self, text="À partir de", font=("Helvetica bold", 13)).grid(row=1, column=3, padx=10, pady=10)
		Label(self, text="Préfixe", font=("Helvetica bold", 13)).grid(row=1, column=4, padx=10, pady=10)
		Label(self, text="Nom du fichier", font=("Helvetica bold", 13)).grid(row=1, column=5, padx=10, pady=10)
		Label(self, text="Suffixe", font=("Helvetica bold", 13)).grid(row=1, column=6, padx=10, pady=10)
		Label(self, text="Extension", font=("Helvetica bold", 13)).grid(row=1, column=7, padx=10, pady=10)
		ligne = 2
		for regle in self.lesRegles.getRegles():
			Label(self, text=regle.getNomRegle(), font=("Helvetica", 13)).grid(row=ligne, column=1, padx=10, pady=10)
			Label(self, text=regle.getAmorce(), font=("Helvetica", 13)).grid(row=ligne, column=2, padx=10, pady=10)
			Label(self, text=regle.getApartirde(), font=("Helvetica", 13)).grid(row=ligne, column=3, padx=10, pady=10)
			Label(self, text=regle.getPrefixe(), font=("Helvetica", 13)).grid(row=ligne, column=4, padx=10, pady=10)
			Label(self, text=regle.getNomFichier(), font=("Helvetica", 13)).grid(row=ligne, column=5, padx=10, pady=10)
			Label(self, text=regle.getPostFixe(), font=("Helvetica", 13)).grid(row=ligne, column=6, padx=10, pady=10)
			Label(self, text=regle.getExtension(), font=("Helvetica", 13)).grid(row=ligne, column=7, padx=10, pady=10)
			self.utiliser = Button(self, text="Utiliser", command=lambda regle=regle: self.traitementListerUtiliser(regle))
			self.utiliser.grid(sticky=N, row=ligne, column=8, padx=10, pady=10)
			self.supprimer = Button(self, text="Supprimer", command=lambda regle=regle: self.traitementListerSupprimer(regle))
			self.supprimer.grid(sticky=N, row=ligne, column=9, padx=10, pady=10)
			ligne += 1
		return True

	def createMenu(self):
		"""
		Méthode s'occupant de créer l'interface du menu de l'application.
		"""
		self.barreMenu = Menu(self)
		self.barreMenu.add_command(label="Renommer", command=self.fenetreRenommerRepertoire)
		self.regles = Menu(self.barreMenu, tearoff=0)
		self.regles.add_command(label="Lister", command=self.fenetreListerRegle)
		self.regles.add_command(label="Creer", command=self.fenetreCreerRegle)
		self.barreMenu.add_cascade(label="Règles", menu=self.regles)
		self.barreMenu.add_command(label="?", command=self.aide)
		self.config(menu=self.barreMenu)
		return True

	def selectBoutonNouveauNom(self, event):
		"""
		Permet de sélectionner automatiquement le bouton du champ nouveau nom lors de l'entrée de l'utilisateur dans le champ du nouveau nom.
		"""
		try:
			self.boutonNouveauNom.select()
		except Exception as e:
			return False
		else:
			return True

	def clearScreen(self):
		"""
		Supprime tous les objets de la page ainsi que les paramètres de la grille.
		Sert de transition entre les écrans.
		"""
		try:
			for widget in self.winfo_children():
				widget.grid_remove()
				widget.destroy()
		except Exception as e:
			return False
		else:
			return True

	def traitementCreer(self):
		"""
		Méthode permettant le traitement de l'appui de l'utilisateur sur le bouton 'créer une règle'.
		Cette méthode s'occupe de gérer les injections, et renvoie une liste d'erreurs en cas de problèmes.
		Sinon la règle est ajoutée à la liste de règles et dans le fichier RenomTom.ini.
		"""
		enregistrer = True
		erreur = []
		nomRegle = "Règle Actuelle"
		try:
			for widget in self.erreursLabels:
				widget.grid_remove()
				widget.destroy()
		except Exception as e:
			pass
		self.erreursLabels = []

		if self.regle.get() == "" or self.regle.get() == None :
			erreur.append("Il manque le nom de la règle.")
			enregistrer = False
		else:
			nomRegle = self.regle.get()

		if self.amorce.curselection()[0] == 0:
			amorce = "aucun"
			aPartirDe = ""
		elif self.amorce.curselection()[0] == 1:
			amorce = "lettre"
			if self.aPartirDe.get() != "":
				if re.match('^.*([A-Z].*)$', self.aPartirDe.get()):
					aPartirDe = self.aPartirDe.get()
				else:
					erreur.append("A partir de doit être une suite de lettres majuscules (Ex : 'ADZ').")
					enregistrer = False
			else:
				aPartirDe = "A"
		elif self.amorce.curselection()[0] == 2:
			amorce = "chiffre"
			if self.aPartirDe.get() != "":
				try:
					aPartirDe = int(self.aPartirDe.get())
				except Exception:
					erreur.append("A partir de doit être un entier.")
					enregistrer = False
		
		if self.checkRadio.get() == 2:
			choixNomFichier = "True"
		else:
			choixNomFichier = "False"
		if self.checkRadio.get() != 2 and self.checkRadio.get() != 1:
			erreur.append("Choisisser un mode pour le nom du fichier.")
			enregistrer = False
		if self.checkRadio.get() == 2:
			if self.nomFichier.get() == "" or self.nomFichier.get() == None :
				nomFichier = ""
			else:
				nomFichier = self.nomFichier.get()
		else:
			nomFichier = ""
		
		prefixe = self.prefixe.get()
		suffixe = self.suffixe.get()
		extension = self.extension.get()

		if enregistrer:
			for element in [nomRegle, str(aPartirDe), prefixe, nomFichier, suffixe, extension]:
				for test in ["\\", "/", "*", "?", "\"", "<", ">", "|", "'"]:
					if test in element:
						erreur.append("Interdit de mettre des \", /, *, ?, \", <, >, | et ' dans les champs !")
						enregistrer = False

		if enregistrer:
			self.lesRegles.ajouterRegle(Regle(nomRegle, amorce, aPartirDe, prefixe, choixNomFichier, nomFichier, suffixe, extension)).sauvegarder()
			self.fenetreListerRegle()
			return True
		else:
			monLabel = Label(self, text="Erreur : ", font=("Helvetica red", 16))
			self.erreursLabels.append(monLabel)
			monLabel.grid(sticky=W, row=14, column=1, columnspan=10, padx=10, pady=10)
			compteur = 15
			for uneErreur in erreur:
				monLabel = Label(self, text=" - " + uneErreur, font=("Helvetica red", 13))
				self.erreursLabels.append(monLabel)
				monLabel.grid(sticky=W, row=compteur, column=1, columnspan=10, padx=10, pady=10)
				compteur += 1
			return False

	def traitementRenommer(self):
		"""
		Méthode permettant le traitement de l'appui de l'utilisateur sur le bouton 'Renommer un répertoire'.
		Cette méthode s'occupe de gérer les injections, et renvoie une liste d'erreurs en cas de problèmes.
		Sinon le répertoire est modifié suivant les règles.
		"""
		erreur = []
		enregistrer = True
		nomRegle = "Règle Actuelle"
		try:
			for widget in self.erreursLabels:
				widget.grid_remove()
				widget.destroy()
		except Exception as e:
			pass
		try:
			self.champAucuneAmorceValidation.grid_remove()
			self.champAucuneAmorceValidation.destroy()
			del self.champAucuneAmorceValidation
		except Exception as e:
			pass
		try:
			self.succes.grid_remove()
			self.succes.destroy()
		except Exception as e:
			pass

		self.erreursLabels = []
		if self.nomRepertoire.get() == "" or self.nomRepertoire.get() == None :
			erreur.append("Aucun nom de répertoire !")
			enregistrer = False
		if not os.path.exists(os.path.dirname(self.nomRepertoire.get())):
			erreur.append("Impossible de trouver le répertoire !")
			enregistrer = False
		else:
			nomRepertoire = self.nomRepertoire.get()

		if self.amorce.curselection()[0] == 0:
			self.champAucuneAmorceValidation = Label(self, text="Attention : sans amorce, seul le premier fichier a été renommé !", font=("Helvetica green", 16))
			self.champAucuneAmorceValidation.grid(sticky=E, row=14, column=1, columnspan=5, padx=10, pady=10)
			amorce = "aucun"
			aPartirDe = ""
		elif self.amorce.curselection()[0] == 1:
			amorce = "lettre"
			if self.aPartirDe.get() != "":
				if re.match('^.*([A-Z].*)$', self.aPartirDe.get()):
					aPartirDe = self.aPartirDe.get()
				else:
					erreur.append("A partir de doit être une suite de lettres majuscules (Ex : 'ADZ').")
					enregistrer = False
			else:
				aPartirDe = "A"
		elif self.amorce.curselection()[0] == 2:
			amorce = "chiffre"
			if self.aPartirDe.get() != "":
				try:
					aPartirDe = int(self.aPartirDe.get())
				except Exception:
					erreur.append("A partir de doit être un entier.")
					enregistrer = False
			else:
				aPartirDe = 0
		if self.checkRadio.get() == 2:
			choixNomFichier = "True"
		else:
			choixNomFichier = "False"
		if self.checkRadio.get() == 2:
			if self.nomFichier.get() == "" or self.nomFichier.get() == None :
				nomFichier = ""
			else:
				nomFichier = self.nomFichier.get()
		else:
			nomFichier = ""
		
		prefixe = self.prefixe.get()
		suffixe = self.suffixe.get()
		extension = self.extension.get().replace(" ", "")

		if enregistrer:
			for element in [str(aPartirDe), prefixe, nomFichier, suffixe, extension]:
				for test in ["\\", "/", "*", "?", "\"", "<", ">", "|", "'"]:
					if test in element:
						erreur.append("Interdit de mettre des \", /, *, ?, \", <, >, | et ' dans les champs !")
						enregistrer = False

		if enregistrer:
			self.regleRenommage = Regle(nomRegle, amorce, aPartirDe, prefixe, choixNomFichier, nomFichier, suffixe, extension)
			Renommage(nomRepertoire, self.regleRenommage).renommer()
			if not hasattr(self, 'champAucuneAmorceValidation'):
				self.succes = Label(self, text="Renommage réalisé avec succès", font=("Helvetica green", 16))
				self.succes.grid(row=14, column=1, columnspan=10, padx=10, pady=10)
			return True
		else:
			monLabel = Label(self, text="Erreur : ", font=("Helvetica red", 16))
			self.erreursLabels.append(monLabel)
			monLabel.grid(sticky=W, row=14, column=1, columnspan=10, padx=10, pady=10)
			compteur = 15
			for uneErreur in erreur:
				monLabel = Label(self, text=" - " + uneErreur, font=("Helvetica red", 13))
				self.erreursLabels.append(monLabel)
				monLabel.grid(sticky=W, row=compteur, column=1, columnspan=10, padx=10, pady=10)
				compteur += 1
			return False

	def traitementListerUtiliser(self, regle):
		"""
		Traitement de l'appui sur le bouton utiliser de la fenetre lister règles.
		Ce traitement affiche la page de renommage et rempli les champs avec les éléments de la règle passée en paramètres.
		"""
		self.fenetreRenommerRepertoire()
		if regle.getAmorce() == "aucun":
			self.amorce.select_set(0)
		elif regle.getAmorce() == "lettre":
			self.amorce.selection_clear(0)
			self.amorce.select_set(1)
		elif regle.getAmorce() == "chiffre":
			self.amorce.selection_clear(0)
			self.amorce.select_set(2)
		self.aPartirDe.insert(0, regle.getApartirde())
		self.prefixe.insert(0, regle.getPrefixe())
		if regle.getchoixNomFichier():
			self.boutonNomOriginal.deselect()
			self.boutonNouveauNom.select()
			self.nomFichier.insert(0, regle.getNomFichier())
			self.nomFichier.bind('<Button-1>', self.selectBoutonNouveauNom)
		else:
			self.boutonNomOriginal.select()
			self.boutonNouveauNom.deselect()
		self.suffixe.insert(0, regle.getPostFixe())
		self.extension.insert(0, regle.calculExtensionChaine())
		self.previsualisation()

	def traitementListerSupprimer(self, regle):
		"""
		Traitement s'occupant de la suppression de la règle lors de l'appuie sur le bouton 'Supprimer' de la page lister règles.
		Elle s'ocuppe également de la supprimer du fichier, et de la liste de règles actuelle.
		Elle actualise aussi l'écran afin de ne plus avoir la règle supprimée sur l'affichage.
		"""
		self.clearScreen()
		self.createMenu()
		self.lesRegles.supprimerRegle(regle).sauvegarder()
		self.fenetreListerRegle()
		return True

	def aide(self):
		"""
		Affiche l'aide de l'application avec un copyright et le nom du développeur (Moi =) )
		Petit clin d'oeil à Petyr Baelish 'Littlefinger' de Game of Thrones parce que commenter c'est pas drôle.
		"""
		self.clearScreen()
		self.createMenu()
		self.title("RenomTom - Informations")

		Label(self, text="Application réalisée par BERNE Thomas.", font=("Helvetica", 16)).grid(row=1, column=1, padx=10, pady=10)
		Label(self, text="Le chaos est une échelle", font=("Helvetica", 12)).grid(row=2, column=1, padx=10, pady=10)
		Label(self, text="Nombreux sont ceux qui échouent en tentant de la gravir", font=("Helvetica", 12)).grid(row=3, column=1, padx=10, pady=10)
		Label(self, text="Et qui n'ont plus jamais l'occasion d'essayer.", font=("Helvetica", 12)).grid(row=4, column=1, padx=10, pady=10)
		Label(self, text="La chute les brise", font=("Helvetica", 12)).grid(row=5, column=1, padx=10, pady=10)
		Label(self, text="Et certains ont l'occasion de la gravir", font=("Helvetica", 12)).grid(row=6, column=1, padx=10, pady=10)
		Label(self, text="Mais s'y refusent", font=("Helvetica", 12)).grid(row=7, column=1, padx=10, pady=10)
		Label(self, text="Ils s'accrochent au code", font=("Helvetica", 12)).grid(row=8, column=1, padx=10, pady=10)
		Label(self, text="Ou à la cybersécurité", font=("Helvetica", 12)).grid(row=9, column=1, padx=10, pady=10)
		Label(self, text="Ou au Web", font=("Helvetica", 12)).grid(row=10, column=1, padx=10, pady=10)
		Label(self, text="Illusion que tous cela", font=("Helvetica", 15)).grid(row=11, column=1, padx=10, pady=15)
		Label(self, text="L'échelle seule existe", font=("Helvetica", 12)).grid(row=12, column=1, padx=10, pady=10)
		Label(self, text="L'ascension est la seule réalité", font=("Helvetica", 12)).grid(row=13, column=1, padx=10, pady=10)
		Label(self, text="Copyleft réservé pour les droits à l'exploitation et à l'utilisation.", font=("", 11)).grid(sticky=E, row=14, column=1, padx=10, pady=10)


	def creerListe(self, listeElems):
		"""
		Permet de créer une listebox. Simplement pour me faciliter la vie.
		"""
		liste = Listbox(self, exportselection=False, height=3, selectmode=SINGLE)
		for valeur in range(len(listeElems)):
			liste.insert(valeur + 1, listeElems[valeur])
		liste.select_set(0)
		return liste