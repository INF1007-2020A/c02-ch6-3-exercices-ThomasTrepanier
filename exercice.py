#!/usr/bin/env python
# -*- coding: utf-8 -*-


def check_brackets(text, brackets):
	#TODO: Associer fermantes à ouvrante
	dictBrackets = {brackets[i] : brackets[i+1] for i in range(0, len(brackets), 2)}

	bracketStack = []
	i = 0
	bracketStack.append(text[i])

	while(len(bracketStack) > 0):
		i += 1
		if(i >= len(text)): return False

		if(text[i] in dictBrackets):
			bracketStack.append(text[i])
		elif (text[i] in dictBrackets.values()):
			lastBracket = bracketStack.pop()
			if(dictBrackets[lastBracket] != text[i]): return False

	return len(bracketStack) == 0

def remove_comments(full_text, comment_start, comment_end):
	while True:
		nextCommentStartId = full_text.find(comment_start)
		nextCommentEndId = full_text.find(comment_end)

		if(nextCommentStartId == -1 and nextCommentEndId == -1):
			return full_text

		if(nextCommentStartId >= nextCommentEndId or (nextCommentStartId == -1) != (nextCommentEndId == -1)):
			return None

		full_text = full_text[:nextCommentStartId] + full_text[nextCommentEndId + len(comment_end):]

	return ""

def get_tag_prefix(text, opening_tags, closing_tags):
	if text[0] != opening_tags[0][0]:
		return (None, None)

	firstEndBalise = text.find(">")
	balise = text[:firstEndBalise + 1]

	if balise in opening_tags:
		return (balise, None)
	elif balise in closing_tags:
		return (None, balise)

	return (None, None)

def check_tags(full_text, tag_names, comment_tags):

	#1 Enlever comments
	noCommentsText = remove_comments(full_text, comment_tags[0], comment_tags[1])
	if(noCommentsText is None):
		return False

	#2 Créer balises
	balisesOuvrantes = ["<" + tag_names[i] + ">" for i in range(0, len(tag_names))]
	balisesFermantes = ["</" + tag_names[i] + ">" for i in range(0, len(tag_names))]
	#3 ...
	baliseStack = []

	while len(noCommentsText) > 0:
		nextBalise = get_tag_prefix(noCommentsText, tuple(balisesOuvrantes), tuple(balisesFermantes))

		if(nextBalise == (None, None)): #Si on n'a pas de balise en début de ligne
			noCommentsText = noCommentsText[1:] # On avance d'un caractère
		elif nextBalise[0] is not None: #Si on a une balise ouvrante en début de ligne
			baliseStack.append(nextBalise)
			noCommentsText = noCommentsText[len(nextBalise[0]):]

		else: #Si on a une balise fermante en début de ligne
			lastBalise = baliseStack.pop() #On prend la dernière balise ouvrante
			if len(baliseStack) == 0 or balisesOuvrantes.index(lastBalise[0]) == balisesFermantes.index(nextBalise[1]): #Si la balise fermante correspond à la dernière balise ouvrante
				noCommentsText = noCommentsText[len(nextBalise[1]):]
			else:
				return False

	return len(baliseStack) == 0


if __name__ == "__main__":
	brackets = ("(", ")", "{", "}")
	yeet = "(yeet){yeet}"
	yeeet = "({yeet})"
	yeeeet = "({yeet)}"
	yeeeeet = "(yeet"
	print(check_brackets(yeet, brackets))
	print(check_brackets(yeeet, brackets))
	print(check_brackets(yeeeet, brackets))
	print(check_brackets(yeeeeet, brackets))
	print()

	spam = "Hello, /* OOGAH BOOGAH */world!"
	eggs = "Hello, /* OOGAH BOOGAH world!"
	parrot = "Hello, OOGAH BOOGAH*/ world!"
	print(remove_comments(spam, "/*", "*/"))
	print(remove_comments(eggs, "/*", "*/"))
	print(remove_comments(parrot, "/*", "*/"))
	print()

	otags = ("<head>", "<body>", "<h1>")
	ctags = ("</head>", "</body>", "</h1>")
	print(get_tag_prefix("<body><h1>Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("<h1>Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("</h1></body>", otags, ctags))
	print(get_tag_prefix("</body>", otags, ctags))
	print()

	spam = (
		"<html>"
		"  <head>"
		"    <title>"
		"      <!-- Ici j'ai écrit qqch -->"
		"      Example"
		"    </title>"
		"  </head>"
		"  <body>"
		"    <h1>Hello, world</h1>"
		"    <!-- Les tags vides sont ignorés -->"
		"    <br>"
		"    <h1/>"
		"  </body>"
		"</html>"
	)
	eggs = (
		"<html>"
		"  <head>"
		"    <title>"
		"      <!-- Ici j'ai écrit qqch -->"
		"      Example"
		"    <!-- Il manque un end tag"
		"    </title>-->"
		"  </head>"
		"</html>"
	)
	parrot = (
		"<html>"
		"  <head>"
		"    <title>"
		"      Commentaire mal formé -->"
		"      Example"
		"    </title>"
		"  </head>"
		"</html>"
	)
	tags = ("html", "head", "title", "body", "h1")
	comment_tags = ("<!--", "-->")
	print(check_tags(spam, tags, comment_tags))
	print(check_tags(eggs, tags, comment_tags))
	print(check_tags(parrot, tags, comment_tags))
	print()

