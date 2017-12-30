import io
import os
import string
class Action(object):
	"""
	Classe définissant une action à réaliser. Par exemple Renommer un répertoire.
	Cette classe est ouverte à l'ajout de nouvelles actions.
	"""
	def __init__(self, nomDuRepertoire, regle):
		super(Action, self).__init__()
		self.setNomDuRepertoire(nomDuRepertoire)
		self.setRegle(regle)

	def getNomDuRepertoire(self):
		return self.nomDuRepertoire
	def setNomDuRepertoire(self, nomDuRepertoire):
		self.nomDuRepertoire = nomDuRepertoire

	def getRegle(self):
		return self.regle
	def setRegle(self, regle):
		self.regle = regle

	def simule(self):
		"""
		Methode permettant de simuler le renommage d'un répertoire
		"""
		pass

	def __str__(self):
		return self.__dict__()

class Renommage(Action):
	"""docstring for Renommage"""
	def __init__(self, nomDuRepertoire, regle):
		super(Renommage, self).__init__(nomDuRepertoire, regle)
	
	def renommer(self):
		"""
		Methode renommant une liste de fichier d'un repertoire donne suivant une regle predefinie.
		"""
		if self.regle.getAmorce() == "aucun":
			nomAEcrire = ""
		elif self.regle.getAmorce() == "chiffre":
			if self.regle.getApartirde() == '':
				iteration = 0
			else : 
				iteration = int(self.regle.getApartirde())
		else:
			if self.regle.getApartirde() == '':
				iteration = 0
			else : 
				iteration = self.lettreToChiffre(self.regle.getApartirde())
		for filename in os.listdir(self.nomDuRepertoire):
			*nomActuel, extension = filename.split(".")
			if "." + extension in self.regle.getExtension() or self.regle.getExtension() == ['']:
				if self.regle.getAmorce() == "chiffre":
					if iteration < 10:
						nomAEcrire = "00" + str(iteration)
					elif iteration < 100:
						nomAEcrire = "0" + str(iteration)
					else:
						nomAEcrire = str(iteration)
					iteration += 1
				elif self.regle.getAmorce() == "lettre":
					nomAEcrire = self.chiffreToLettre(iteration)
					iteration += 1
				nomAEcrire = nomAEcrire + self.regle.getPrefixe()
				if self.regle.getchoixNomFichier() == False:
					for text in nomActuel:
						nomAEcrire = nomAEcrire + text + "."
				else:
					nomAEcrire += self.regle.getNomFichier()
				nomAEcrire = nomAEcrire + self.regle.getPostFixe() + "." + extension
				try:
					os.rename(self.nomDuRepertoire + "/" + filename, self.nomDuRepertoire + "/" + nomAEcrire)
				except Exception:
					pass
				if self.regle.getAmorce() == "aucun":
					nomAEcrire = ""

	def chiffreToLettre(self, nombre):
		"""
		Methode transformant un nombre en lettres majuscules.
		Par exemple 5 donnera E et 28 donnera AB
		"""
		chaine = ""
		while nombre > 0:
			nombre, retenue = divmod(nombre - 1, 26)
			chaine = chr(65 + retenue) + chaine
		return chaine

	def lettreToChiffre(self, lettres):
		"""
		Methode transformant des lettres majuscules en un nombre.
		Par exemple E donnera 5 et AB donnera 28
		"""
		nombre = 0
		for lettre in lettres:
			if lettre in string.ascii_letters:
				nombre = nombre * 26 + (ord(lettre.upper()) - ord('A')) + 1
		return nombre

	def __str__(self):
		return self.__dict__()

class Regle(object):
	"""
	CLasse des règles.
	Chaques règle possède un nom, une amorce qui peut dépendre d'une position de départ définie par aPartirDe,
	Un préfixe, la possibilité de garder le nom du fichier ou d'en prendre un nouveau. Un nouveau nom de fichier,
	un suffixe (appelé ici postfixe), ainsi qu'une extension.
	Cette classe n'a pour vocation qu'à stocker les règles. Aucun traitement n'y est fait.
	Elle ne contient que les getter, setter et __str__.
	"""
	def __init__(self, nomRegle, amorce, apartirde, prefixe, choixNomFichier, nomFichier, postFixe, extension):
		super(Regle, self).__init__()
		self.setNomRegle(nomRegle)
		self.setAmorce(amorce)
		self.setApartirde(apartirde)
		self.setPrefixe(prefixe)
		self.setchoixNomFichier(choixNomFichier)
		self.setNomFichier(nomFichier)
		self.setPostFixe(postFixe)
		self.setExtension(extension)
	
	def getNomRegle(self):
		return self.nomRegle
	def setNomRegle(self, nomRegle):
		self.nomRegle = nomRegle

	def getAmorce(self):
		return self.amorce
	def setAmorce(self, amorce):
		self.amorce = amorce

	def getApartirde(self):
		return self.apartirde
	def setApartirde(self, apartirde):
		self.apartirde = apartirde

	def getPrefixe(self):
		return self.prefixe
	def setPrefixe(self, prefixe):
		self.prefixe = prefixe

	def getchoixNomFichier(self):
		return self.choixNomFichier
	def setchoixNomFichier(self, choixNomFichier):
		if choixNomFichier == "True":
			self.choixNomFichier = True
		elif choixNomFichier == "False":
			self.choixNomFichier = False
		else:
			raise TypeError

	def getNomFichier(self):
		return self.nomFichier
	def setNomFichier(self, nomFichier):
		if self.getchoixNomFichier():
			self.nomFichier = nomFichier
		else:
			self.nomFichier = None

	def getPostFixe(self):
		return self.postFixe
	def setPostFixe(self, postFixe):
		self.postFixe = postFixe

	def getExtension(self):
		return self.extension
	def setExtension(self, extension):
		self.extension = []
		for extension in extension.split(","):
			if extension[0] == ".":
				self.extension.append(extension)
			else:
				self.extension.append("." + extension)
		 
	
	def calculExtensionChaine(self):
		"""
		Retourne une chaine de caractère correspondant aux extensions.
		"""
		extension = ""
		longueur = len(self.extension)
		for x in self.extension:
			if longueur > 1:
				extension = extension + x + ","
				longueur -= 1
			else:
				extension = extension + x
		return extension

	def __str__(self):
		"""
		Retourne la règle une chaine de caractères correspondant à ce qu'il sera écrit dans le fichier à défaut d'une base de données.
		"""
		return str(self.getNomRegle()) + "|"+ str(self.getAmorce()) + "|"+ str(self.getApartirde()) + "|"+ str(self.getPrefixe()) + "|"+ str(self.getchoixNomFichier()) + "|"+ str(self.getNomFichier()) + "|"+ str(self.getPostFixe()) + "|" + str(self.calculExtensionChaine())

class ListeRegle(object):
	"""
	Classe ListeRegle permettant le traitement du fichier de sauvegarde ainsi que celui de la liste de règles créées.
	Elle prends en paramètres une liste de règles.
	"""
	def __init__(self, regles=None):
		super(ListeRegle, self).__init__()
		self.setRegles(regles)
	
	def getRegles(self):
		return self.regles
	def setRegles(self, regles):
		self.regles = regles

	def ajouterRegle(self, maRegle):
		"""
		Permet d'ajouter une règle dans la liste de règles
		"""
		self.regles.append(maRegle)
		return self

	def charger(self):
		"""
		Permet de récupérer les régles dans le fichier RenomTom.ini positionné dans le dossier File_saved.
		Cette méthode retourne l'objet actuel pour des traitements futurs.
		"""
		mesRegles = []
		file = io.open("RenomTom_sauvegarde.ini", "r+", encoding="ISO-8859-1")
		for regle in file.readlines():
			regleTab = regle.replace("\n","").split("|")
			mesRegles.append(Regle(regleTab[0], regleTab[1], regleTab[2], regleTab[3], regleTab[4], regleTab[5], regleTab[6], regleTab[7]))
		self.setRegles(mesRegles)
		file.close()
		return self

	def sauvegarder(self):
		"""
		Permet de sauvegarder la liste de règle actuelle dans le fichier RenomTom.ini positionné dans le dossier File_saved.
		Cette méthode retourne l'objet actuel pour des traitements futurs.
		"""
		file = open("RenomTom.ini", "w")
		for regle in self.regles:
			file.write(str(regle) + "\n")
		file.close()
		return self

	def supprimerRegle(self, regle):
		"""
		Supprime toutes les règles dans la liste de règles semblables à la règle passée en paramètes.
		Cette méthode retourne l'objet actuel pour des traitements futurs.
		"""
		nouvelleListe = []
		for regleTest in self.getRegles():
			if str(regleTest) != str(regle):
				nouvelleListe.append(regleTest)
		self.setRegles(nouvelleListe)
		return self

	def __str__(self):
		return self.__dict__()
