import random
from PIL import Image

from quests import Quest, Action
from .playfair_companies import companies

corpo_job_titles = {
    "Arcane Arts Consultant": {
        "salary": (100, 120),
        "intelligence_requirement": 90,
    },
    "Ontology Engineer": {
        "salary": (40, 80),
        "intelligence_requirement": 70,
    },
    "Junior Assistant": {
        "salary": (10, 30),
        "intelligence_requirement": 40,
    },
    "Astral Project Manager": {
        "salary": (20, 50),
        "intelligence_requirement": 50,
    },
    "Lorekeeper": {
        "salary": (10, 25),
        "intelligence_requirement": 35,
    }
}


def generate_corpo_job():
    employer = random.choice(["Aero Import-Export", "Fissioncasters International", "Solid State Wizardry"])
    title = random.choice(list(corpo_job_titles.keys()))
    salary = random.randint(*corpo_job_titles[title]["salary"])
    intelligence_requirement = corpo_job_titles[title]["intelligence_requirement"]
    job_dict = {'Employer': employer,
                'Title': title,
                'Salary': salary,
                'Wisdom': intelligence_requirement,
                'Strength': None,
                'Action': "Apply for the job.",
                'Raise_possible': True}
    return job_dict


class JobBoard(Quest):
    def __init__(self, playfair_jobs):
        super().__init__()
        self.title = "Job board."
        self.content = ("Companies and enterprises of Playfair announce their open positions here.  \r"
                        ":red-background[Warning:] If you're already employed, accepting a new job will mean quitting the old one.")
        for job in playfair_jobs:
            self.actions[job] = JobAction(job, playfair_jobs[job])


class JobAction(Action):
    def __init__(self, key, job):
        super().__init__()

        self.content = (
            f":blue-background[**{job['Title']}** at {job['Employer']}.] {companies[job['Employer']]['short_description']}"
            f"  \r   \r :moneybag: {job['Salary']} coins/shift  \r ")
        if 'Requirements' in job:
            for req in job['Requirements']:
                if req == "Licensed Physician":
                    self.content += ("  \r This job requires to be a licensed physician, with documents possible to "
                                     "obtain at Patrician's Palace.")
        if job['Strength'] is not None:
            self.content += f"  \r :muscle: Only robust workmen (*{job['Strength']}+ Strength*) will be considered."
        if job['Wisdom'] is not None:
            self.content += f"  \r :brain: Only candidates with high intelligence (*{job['Wisdom']}+ Wisdom*) will be considered."
        if not job['Raise_possible']:
            self.content += "  \r :red-background[It is impossible to get a raise at this job.]"
        self.button = job['Action']
        self.image = Image.open(companies[job['Employer']]["image_path"])
        self.key = key

    def execute(self, player, world):
        player.tags.append("in-quest")
        player.tags.append(f"a:{self.key}")


class InterviewQuest(Quest):
    def __init__(self, job, job_key, player):
        super().__init__()
        self.title = f"Interview at {job['Employer']}."
        self.content += "  \r  \r"
        self.content += companies[job['Employer']]["long_description"]

        if job['Wisdom'] is not None and player.abilities["Wisdom"] < job['Wisdom']:
            self.content += (
                "  \r  \r :red-background[The interviewer asks you a few questions and it soon becomes clear that you"
                " are not smart enough for the position.] Apply again later.")
            self.actions["exit"] = ExitInterviewAction("Too bad.", job_key)
        elif job['Strength'] is not None and player.abilities["Strength"] < job['Strength']:
            self.content += (
                "  \r  \r :red-background[The interviewer evaluates your posture and sees that you are too weak to handle the demands of the job.] Apply again later.")
            self.actions["exit"] = ExitInterviewAction("Too bad.", job_key)
        else:
            passed = True
            if 'Requirements' in job:
                for req in job['Requirements']:
                    if req == "Licensed Physician" and "Licensed Physician" not in player.traits:
                        passed = False
                        self.content += (
                            "\r  \r :red-background[The interviewer is disappointed in your lack of credentials.] Apply "
                            "again with permission of Patrician.")
                        self.actions["exit"] = ExitInterviewAction("Too bad.", job_key)

            if passed:
                self.content += (
                    "  \r  \r :green-background[The interviewer asks you a few question and seems satisfied with your answers.] They"
                    " put forth an offer.")
                self.actions["accept"] = TakeJobAction(job_key, job)
                self.actions["exit"] = ExitInterviewAction("I changed my mind.", job_key)


class ExitInterviewAction(Action):
    def __init__(self, button, key):
        super().__init__()
        self.button = button
        self.key = key

    def execute(self, player, world):
        player.tags.remove("in-quest")
        player.tags.remove(f"a:{self.key}")


class TakeJobAction(Action):
    def __init__(self, key, job):
        super().__init__()
        self.key = key
        self.content = (f":blue-background[**{job['Title']}** at {job['Employer']}.]")
        self.content += (f" :moneybag: {job['Salary']} coins/shift")
        self.button = "I accept."

    def execute(self, player, world):
        player.tags.remove("in-quest")
        player.tags.remove(f"a:{self.key}")
        for company in companies:
            if companies[company]["employee_trait"] in player.traits:
                player.traits.remove(companies[company]["employee_trait"])
        new_job = world.playfair_jobs[self.key]
        new_job['Last_raise'] = world.state["Day"]
        player.job = new_job

        player.traits.append(companies[world.playfair_jobs[self.key]['Employer']]["employee_trait"])
        player.tags.append("employed")
        world.message = f":green-background[You got hired as {world.playfair_jobs[self.key]['Title']} at {world.playfair_jobs[self.key]['Employer']}]"
        if "corpo" in self.key:
            world.playfair_jobs[self.key] = generate_corpo_job()


class EmploymentQuest(Quest):
    def __init__(self, player, current_day):
        super().__init__()
        if player.job is not None:
            days_at_job = current_day - player.job['Last_raise']
            self.title = f"Employment at {player.job['Employer']}"
            self.content = (
                f"Job: :blue-background[{player.job['Title']}]  \r :moneybag: Salary: {player.job['Salary']} coins/shift  "
                f"\r :clock1: {days_at_job} days since last promotion.")
            self.actions["work"] = WorkShiftAction(player.job)
            if player.job['Raise_possible']:
                if "negotiated_today" not in player.tags:
                    self.actions["negotiate"] = NegotiateRaiseAction(days_at_job, player)
            else:
                self.content += "  \r :red-background[It is impossible to get a raise at this job.]"
            self.actions["quit"] = QuitJobAction()


class QuitJobAction(Action):
    def __init__(self):
        super().__init__()
        self.button = "Quit."

    def execute(self, player, world):
        for company in companies:
            if companies[company]["employee_trait"] in player.traits:
                player.traits.remove(companies[company]["employee_trait"])
        world.message = f":blue-background[You quit your job as {player.job['Title']} at {player.job['Employer']}.]"
        player.tags.remove("employed")
        player.job = None
        if "negotiated_today" in player.tags:
            player.tags.remove("negotiated_today")


class WorkShiftAction(Action):
    def __init__(self, job):
        super().__init__()
        self.button = "Work a shift."
        self.image = Image.open(companies[job['Employer']]["image_path"])

    def execute(self, player, world):
        if player.personality["Energy"] <= 20:
            world.message = ":red-background[You are too exhausted to work.]"
            return None
        salary = player.job['Salary']
        if player.job['Title'] == "Manual worker":
            world.message = f"You worked a shift at your job as {player.job['Title']} at {player.job['Employer']}."
            toss = random.randint(1, 100)
            world.message += f"  \r Strength test: {toss} / {player.abilities['Strength'] + 20} ({player.abilities['Strength']} Strength + 20)"
            if toss < player.abilities["Strength"] + 20:
                world.message += " :green-background[(Passed)]"
            else:
                world.message += " :red-background[(Failed)  \r The bossman docked your pay by 2 coins.]"
                salary -= 2
            if toss < player.abilities["Strength"]:
                bonus = random.randint(1, 4)
                world.message += f"  \r Boss is impressed by your work and gives you a small bonus today ({bonus})."
                salary += bonus
            world.message += f"  \r You earned :moneybag: {salary} coins."
            strength_bonus = random.randint(0, 1)
            if strength_bonus > 0:
                player.abilities['Strength'] += strength_bonus
                world.message += f"  \r  \r Your Strength grew by {strength_bonus} from the physical activity."
            exhaustion_gain = random.randint(20, 40)
            player.personality["Energy"] -= exhaustion_gain
            world.message += f"  \r  Your Energy decreased by {exhaustion_gain}."
        else:
            world.message = f"You worked a shift at your job as {player.job['Title']} at {player.job['Employer']}.  \r :green-background[You earned {salary} coins.]"
            exhaustion_gain = random.randint(10, 25)
            player.personality["Energy"] -= exhaustion_gain
            world.message += f"  \r  Your Energy decreased by {exhaustion_gain}."
        dedication_gain = random.randint(1, 3)
        player.personality["Dedication"] += dedication_gain
        world.message += f"  \r  Your Dedication increased by {dedication_gain}."
        player.money += salary
        super().execute(player, world)


class NegotiateRaiseAction(Action):
    def __init__(self, days_at_job, player):
        super().__init__()
        if days_at_job < 2:
            test = (-80, ":red-background[impossible]")
        elif days_at_job < 4:
            test = (-40, ":red-background[very hard]")
        elif days_at_job < 6:
            test = (-10, ":red-background[hard]")
        elif days_at_job < 9:
            test = (+0, ":blue-background[alright]")
        else:
            test = (+20, ":green-background[easy]")
        self.odds = max(0, player.abilities["Charisma"] + test[0] - 10)
        self.content = (f"It will be {test[1]} ({test[0]}) to negotiate a raise, as you got one (or got employed"
                        f") {days_at_job} days ago.  \r :blue-background[Odds of success: {self.odds}%] ({player.abilities['Charisma']} Charisma + ({test[0]}) {test[1]} - 10 Employer)")
        self.button = "Negotiate a raise."

    def execute(self, player, world):
        player.tags.append("negotiated_today")
        toss = random.randint(1, 100)
        if toss <= self.odds:
            old_salary = player.job['Salary']
            bonus = min(20, random.randint(1, 3) + old_salary // 15)
            player.job['Salary'] = old_salary + bonus
            player.job['Last_raise'] = world.state["Day"]
            world.message = f":green-background[You successfully negotiated a raise by {bonus} coins per shift!]  \r :moneybag: Salary at {player.job['Employer']}: {old_salary} => {player.job['Salary']}"
        else:
            world.message = f":red-background[You did not manage to get a raise.]"
