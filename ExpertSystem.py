import json
class ExpertSystem:
    def __init__(self):
        self.diagnosis = None
        self.self_care = None
        with open("questionsFormate.json") as json_file:
            self.questions = json.load(json_file)
        self.conditions = []
        
        self.run()

    def ask_question(self, question, allowed_values):
        answer = input(question).lower()
        while answer not in allowed_values:
            answer = input(question).lower()
        return answer

    def yes_or_no_p(self, question):
        response = self.ask_question(question, ["yes", "no"])
        return response == "yes"
    
    def questionne(self, question):
        question["visible"] = False
        match question["type"]:
            case "yes-or-no-p":
                if self.yes_or_no_p(question["question"]) == True:
                    a = "then"
                else : 
                    a = "else"
                for ITEM in question[a]:
                    if ITEM["assertType"] == "diagnosis":
                        self.diagnosis = ITEM["assertation"]
                    elif ITEM["assertType"] == "self-care":
                        self.self_care = ITEM["assertation"]
                    elif ITEM["assertType"] == "condition":
                        self.conditions.append(ITEM)
                    else:
                        print("Erreur, type d'assertion inconnu")
                        return
                return
            case "a-b-c-d":
                print("Mettre ici les autres types de questions")
                return

    def run(self):
        #Au maximum, le code posera chaque question dans l'ordre inverse de la liste
        for i in range(len(self.questions)):
            #On cherche une question non posée, pour ce faire on cherche une question qui est visible
            for question in self.questions:
                #Si la question n'est pas visible, on la passe
                if (self.questions[question]["visible"] == False): continue
                #Si les conditions de la question ne sont pas remplies, on la passe
                possible = True
                for condition in self.questions[question]["conditions"]:
                    valide = False
                    for cond in self.conditions:
                        if condition["condition"] == cond["condition"]:
                            if condition["value"] == cond["value"]:
                                valide = True
                                break
                    if not valide:
                        possible = False
                        break
                
                #Si la question est visible les conditions sont remplies, on pose la question
                if not possible: continue
                else : self.questionne(self.questions[question])

                #Si on a un diagnostic, on l'affiche et on quitte
                if self.diagnosis != None:
                    print("Votre diagnostic est : " + self.diagnosis)
                    if self.self_care is not None : print("Conseil : " + self.self_care)
                    return

if __name__ == "__main__":
    ExpertSystem()