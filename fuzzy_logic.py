class TrapeizodalMembershipFunction:

    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.center = None

        self.calculate_centroid_trapezoid()

    def calculate(self, x):
        if x < self.a or x > self.d:
            return 0
        elif self.a <= x <= self.b:
            try:
                return (x - self.a) / (self.b - self.a)
            except ZeroDivisionError:
                return 1
        elif self.b < x <= self.c:
            return 1
        elif self.c < x < self.d:
            try:
                return (self.d - x) / (self.d - self.c)
            except ZeroDivisionError:
                return 1
        return 0
    
    def calculate_centroid_trapezoid(self):
        """
        Calculate the centroid of a trapezoid with height 1.
        :param a: Start of the lower base of the trapezoid.
        :param b: Start of the upper base of the trapezoid.
        :param c: End of the upper base of the trapezoid.
        :param d: End of the lower base of the trapezoid.
        :return: Centroid x-coordinate.
        """
        # Divide the entire trapezoid into 10 parts
        step = int((self.d - self.a) / 10)  + 1
        x_values = range(int(self.a), int(self.d + step), int(step))

        # Calculate membership function (piecewise linear increase/decrease)
        mu_values = []
        for x in x_values:
            if self.a <= x < self.b:
                mu = (x - self.a) / (self.b - self.a)
            elif self.b <= x <= self.c:
                mu = 1
            elif self.c < x <= self.d:
                mu = (self.d - x) / (self.d - self.c)
            else:
                mu = 0
            mu_values.append(mu)

        # Compute weighted average for centroid
        numerator = sum(x * mu for x, mu in zip(x_values, mu_values))
        denominator = sum(mu_values)

        self.center = numerator / denominator

    def get_trapezoid_top(self, h):
        """
        Verilen yükseklik h ile yamuğun tabanindan kesilen yamuk için tavanin
        başlangiç ve bitiş koordinatlarini döndüren fonksiyon.
        :param h: Kesilen yamuğun yüksekliği (0 ile 1 arasinda).
        :return: Tavanin başlangiç ve bitiş koordinatlari.
        """
        # Üçgenin orijinal taban uzunluğu
        base_length = self.d - self.a
        
        # Üst kenarin uzunluğu, orantili olarak küçülür
        top_length = base_length * h
        
        # Üst kenarin başlangiç ve bitiş koordinatlarini hesapla
        # Başlangiç noktasi: a + (base_length - top_length) / 2
        # Bitiş noktasi: c - (base_length - top_length) / 2
        start_of_top = self.a + (base_length - top_length) / 2
        end_of_top = self.d - (base_length - top_length) / 2
        
        return start_of_top, end_of_top


class TriangularMembershipFunction:
    
    def __init__(self, a, b, c): # (7,10,10) x=9
        self.a = a
        self.b = b
        self.c = c
        self.d = c
        self.center = None

        self.calculate_centroid_triangle()

    def calculate(self, x):
        if x < self.a or x > self.c:
            return 0
        elif self.a <= x <= self.b:
            try:
                return (x - self.a) / (self.b - self.a)
            except ZeroDivisionError:
                return 1
        elif self.b < x < self.c:
            try:
                return (self.c - x) / (self.c - self.b)
            except ZeroDivisionError:
                return 1
        return 0
    
    def get_trapezoid_top(self, h):
        """
        Verilen yükseklik h ile üçgenin tabanindan kesilen yamuk için tavanin
        başlangiç ve bitiş koordinatlarini döndüren fonksiyon.
        :param h: Kesilen üçgenin yüksekliği (0 ile 1 arasinda).
        :return: Tavanin başlangiç ve bitiş koordinatlari.
        """
        # Üçgenin orijinal taban uzunluğu
        base_length = self.c - self.a
        
        # Üst kenarin uzunluğu, orantili olarak küçülür
        top_length = base_length * h
        
        # Üst kenarin başlangiç ve bitiş koordinatlarini hesapla
        # Başlangic noktasi: a + (base_length - top_length) / 2
        # Bitiş noktasi: c - (base_length - top_length) / 2
        start_of_top = self.a + (base_length - top_length) / 2
        end_of_top = self.c - (base_length - top_length) / 2
        
        return start_of_top, end_of_top
    
    def calculate_centroid_triangle(self, height = 1):
        """
        Calculate the centroid of a triangle with height 1.
        :param a: Start of the base of the triangle (x-coordinate).
        :param b: End of the base of the triangle (x-coordinate).
        :return: Centroid x-coordinate.
        """
        center = (self.a + self.c) / 2

        center = (center + center + self.b) / 3

        self.center = center

class FuzzyVariable:

    def __init__(self, name):
        self.name = name
        self.memberships = {}

    def add_membership(self, label, membership_function):
        self.memberships[label] = membership_function
        
    def calculate_membership_degrees(self, x):
        results = {}
        for label, func in self.memberships.items():
            degree = func.calculate(x)
            results[label] = degree
        return results

    def __str__(self):
        memberships = ", ".join([f"{label}: {str(func)}" for label, func in self.memberships.items()])
        return f"FuzzyVariable(name={self.name}, memberships={{ {memberships} }})"


class FuzzyRule:

    def __init__(self, condition, output_label):
        self.condition = condition
        self.output_label = output_label

    def evaluate(self, inputs):
        return self.condition(inputs)


class FuzzySystem:

    def __init__(self):
        self.input_variables = {}
        self.output_variables = {}
        self.input_rules = []
        self.output_rules = []

    def add_input_variable(self, variable):
        self.input_variables[variable.name] = variable

    def add_output_variable(self, variable):
        self.output_variables[variable.name] = variable

    def add_rule(self, rule, input_flag=0):
        if input_flag == 0:
            self.input_rules.append(rule)
        elif input_flag == 1:
            self.output_rules.append(rule)

    def evaluate(self, inputs, second_phase = False):
        rule_outputs = []
        intermediate_outputs = {}

        for rule in self.input_rules:
            rule_strength = rule.evaluate(inputs)
            rule_outputs.append((rule_strength, rule.output_label))
            output_name =  rule.output_label.split(".")[0]
            if output_name in intermediate_outputs:
                if intermediate_outputs[output_name] < rule_strength:
                    intermediate_outputs[output_name] = rule_strength
            else:
                intermediate_outputs[output_name] = rule_strength

        if second_phase == True:
            new_inputs = intermediate_outputs | inputs
            for rule in (self.output_rules + self.input_rules):
                rule_strength = rule.evaluate(new_inputs)
                rule_outputs.append((rule_strength, rule.output_label))
                if "Credit" in rule.output_label: 
                    #print(rule.output_label, rule_strength)
                    ""

        # TODO
        # Combine the results for each output
        output_values = {name: [0] * len(var.memberships) for name, var in self.output_variables.items()}
        for strength, output_label in rule_outputs:
            var_name, membership_label,a = output_label.split('.')
            index = list(self.output_variables[var_name].memberships.keys()).index(membership_label)
            output_values[var_name][index] = max(output_values[var_name][index], strength)
            
        # print("AAAAAAAAAAAAAA")
        # print(output_values)
        

        # Defuzzify the results
        results = {}
        for name, var in self.output_variables.items():
            height_list = output_values[name]
            for key in self.output_variables[name].memberships.keys():
                index = list(self.output_variables[name].memberships.keys()).index(key)
                height = height_list[index]
                temp_func = self.output_variables[name].memberships[key]
                if (height > 0.05) and (abs(height - 1) > 0.05):
                    start, finish = temp_func.get_trapezoid_top(height)
                    temp_func = TrapeizodalMembershipFunction(temp_func.a, start, finish, temp_func.d)
                    self.output_variables[name].memberships[key] = temp_func
            
            values = list(var.memberships.values())
            degrees = self.amplify_weights(output_values[name])
            centers = [func.center for func in values]  # Assume membership center is at `c`
            results[name] = self.centroid_defuzzification(centers, degrees)

        if second_phase == False:
            results = self.evaluate(results | inputs, True)
        return results
    


    @staticmethod
    def centroid_defuzzification(centers, degrees):
        numerator = sum(c * d for c, d in zip(centers, degrees))
        denominator = sum(degrees)
        return numerator / denominator if denominator != 0 else 0
    
    @staticmethod
    def amplify_weights(weights, alpha=1.7):
        """
        Ağirliklari kuvvetlendiren bir yöntem.

        Args:
            weights (list of float): Orijinal ağirliklar.
            alpha (float): Kuvvetlendirme katsayisi (default: 2).

        Returns:
            list of float: Kuvvetlendirilmiş ve normalize edilmiş ağirliklar.
        """
        # Ağirliklari kuvvetlendirme
        amplified_weights = [w**alpha for w in weights]
        
        # Normalizasyon
        total = sum(amplified_weights)
        if total == 0:
            return weights
        
        normalized_weights = [w / total for w in amplified_weights]
        return normalized_weights


class FuzzyControlSystem: 
    """Bulanik kontrol sistemi"""
    def __init__(self):
        self.system = FuzzySystem()
        self.inputs = {}
        self.outputs = {}

    def CreateInputVariables(self):

        """ Input Variables """

        # MarketValue
        marketvalue = FuzzyVariable("MarketValue")
        marketvalue.add_membership("Low", TrapeizodalMembershipFunction(0, 0, 80, 100))
        marketvalue.add_membership("Medium", TrapeizodalMembershipFunction(50, 100, 200, 250))
        marketvalue.add_membership("High", TrapeizodalMembershipFunction(200, 300, 650, 850))
        marketvalue.add_membership("Very High", TrapeizodalMembershipFunction(650, 850, 1000, 1000))
        self.system.add_input_variable(marketvalue)

        # Location
        location = FuzzyVariable("Location")
        location.add_membership("Bad", TrapeizodalMembershipFunction(0, 0, 1.5, 4))
        location.add_membership("Fair", TrapeizodalMembershipFunction(2.5, 5, 6, 8.5))
        location.add_membership("Excellent", TrapeizodalMembershipFunction(6, 8.5, 10, 10))
        self.system.add_input_variable(location)

        # Asset
        asset = FuzzyVariable("Asset")
        asset.add_membership("Low", TriangularMembershipFunction(0, 0, 150))
        asset.add_membership("Medium", TrapeizodalMembershipFunction(50, 250, 450, 650))
        asset.add_membership("High", TrapeizodalMembershipFunction(500, 700, 1000, 1000))
        self.system.add_input_variable(asset)

        # Income
        income = FuzzyVariable("Income")
        income.add_membership("Low", TrapeizodalMembershipFunction(0, 0, 10, 25))
        income.add_membership("Medium", TriangularMembershipFunction(15, 35, 55))
        income.add_membership("High", TriangularMembershipFunction(40, 60, 80))
        income.add_membership("Very High", TrapeizodalMembershipFunction(60, 80, 100, 100))
        self.system.add_input_variable(income)

        # Interest Rate
        interest = FuzzyVariable("Interest")
        interest.add_membership("Low", TrapeizodalMembershipFunction(0, 0, 2, 5))
        interest.add_membership("Medium", TrapeizodalMembershipFunction(2, 4, 6, 8))
        interest.add_membership("High", TrapeizodalMembershipFunction(6, 8.5, 10, 10))
        self.system.add_input_variable(interest)

        return marketvalue, location, asset, income, interest

    def CreateOutputVariables(self):

        """ Output Variables """
        
        # House
        house = FuzzyVariable("House")
        house.add_membership("Very Low", TriangularMembershipFunction(0, 0, 3))
        house.add_membership("Low", TriangularMembershipFunction(0, 3, 6))
        house.add_membership("Medium", TriangularMembershipFunction(2, 5, 8))
        house.add_membership("High", TriangularMembershipFunction(4,7,10))
        house.add_membership("Very High", TriangularMembershipFunction(7, 10, 10))
        self.system.add_output_variable(house)

        # Applicant 
        applicant = FuzzyVariable("Applicant")
        applicant.add_membership("Low", TrapeizodalMembershipFunction(0, 0, 2, 4))
        applicant.add_membership("Medium", TriangularMembershipFunction(2, 5, 8))
        applicant.add_membership("High", TrapeizodalMembershipFunction(6, 8, 10, 10))
        self.system.add_output_variable(applicant)

        # Credit
        credit = FuzzyVariable("Credit")
        credit.add_membership("Very Low", TriangularMembershipFunction(0, 0, 125))
        credit.add_membership("Low", TriangularMembershipFunction(0, 125, 250))
        credit.add_membership("Medium", TriangularMembershipFunction(125, 250, 375))
        credit.add_membership("High", TriangularMembershipFunction(250, 375, 500))
        credit.add_membership("Very High", TriangularMembershipFunction(375, 500, 500))
        self.system.add_output_variable(credit)

        return house, applicant, credit

    """RULES ARE CREATED"""

    def CreateRules(self):

        """HOUSE EVALUATION RULES"""
        # IF "MarketValue" is "Low", THEN "House" is "Low"
        self.system.add_rule(FuzzyRule(
            lambda inputs : 
                self.system.input_variables["MarketValue"].memberships["Low"].calculate(inputs["MarketValue"]),
            "House.Low.1"
        ))
        
        # IF "Location" is "Bad", THEN "House" is "Low"
        self.system.add_rule(FuzzyRule(
            lambda inputs : 
                self.system.input_variables["Location"].memberships["Bad"].calculate(inputs["Location"]),
            "House.Low.2"
        ))        

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Location"].memberships["Bad"].calculate(inputs["Location"]),
                self.system.input_variables["MarketValue"].memberships["Low"].calculate(inputs["MarketValue"])
            ),
            "House.Very Low.1"
        ))    

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Location"].memberships["Bad"].calculate(inputs["Location"]),
                self.system.input_variables["MarketValue"].memberships["Medium"].calculate(inputs["MarketValue"])
            ),
            "House.Low.3"
        ))  

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Location"].memberships["Bad"].calculate(inputs["Location"]),
                self.system.input_variables["MarketValue"].memberships["High"].calculate(inputs["MarketValue"])
            ),
            "House.Medium.1"
        ))  

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Location"].memberships["Bad"].calculate(inputs["Location"]),
                self.system.input_variables["MarketValue"].memberships["Very High"].calculate(inputs["MarketValue"])
            ),
            "House.High.1"
        ))   

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Location"].memberships["Fair"].calculate(inputs["Location"]),
                self.system.input_variables["MarketValue"].memberships["Low"].calculate(inputs["MarketValue"])
            ),
            "House.Low.4"
        ))    

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Location"].memberships["Fair"].calculate(inputs["Location"]),
                self.system.input_variables["MarketValue"].memberships["Medium"].calculate(inputs["MarketValue"])
            ),
            "House.Medium.2"
        ))  

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Location"].memberships["Fair"].calculate(inputs["Location"]),
                self.system.input_variables["MarketValue"].memberships["High"].calculate(inputs["MarketValue"])
            ),
            "House.High.2"
        ))  

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Location"].memberships["Fair"].calculate(inputs["Location"]),
                self.system.input_variables["MarketValue"].memberships["Very High"].calculate(inputs["MarketValue"])
            ),
            "House.Very High.1"
        ))   

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Location"].memberships["Fair"].calculate(inputs["Location"]),
                self.system.input_variables["MarketValue"].memberships["Medium"].calculate(inputs["MarketValue"])
            ),
            "House.Medium.3"
        ))  

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Location"].memberships["Fair"].calculate(inputs["Location"]),
                self.system.input_variables["MarketValue"].memberships["High"].calculate(inputs["MarketValue"])
            ),
            "House.High.3"
        ))  



        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Location"].memberships["Excellent"].calculate(inputs["Location"]),
                self.system.input_variables["MarketValue"].memberships["Medium"].calculate(inputs["MarketValue"])
            ),
            "House.Medium.4"
        ))  

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Location"].memberships["Excellent"].calculate(inputs["Location"]),
                self.system.input_variables["MarketValue"].memberships["High"].calculate(inputs["MarketValue"])
            ),
            "House.High.4"
        ))  

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Location"].memberships["Excellent"].calculate(inputs["Location"]),
                self.system.input_variables["MarketValue"].memberships["Very High"].calculate(inputs["MarketValue"])
            ),
            "House.Very High.2"
        ))  

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Location"].memberships["Excellent"].calculate(inputs["Location"]),
                self.system.input_variables["MarketValue"].memberships["Low"].calculate(inputs["MarketValue"])
            ),
            "House.Medium.5"
        )) 


        """ APPLICATION EVALUATION RULES """
        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Asset"].memberships["Low"].calculate(inputs["Asset"]),
                self.system.input_variables["Income"].memberships["Low"].calculate(inputs["Income"])
            ),
            "Applicant.Low.1"
        )) 

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Asset"].memberships["Low"].calculate(inputs["Asset"]),
                self.system.input_variables["Income"].memberships["Medium"].calculate(inputs["Income"])
            ),
            "Applicant.Low.2"
        )) 

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Asset"].memberships["Low"].calculate(inputs["Asset"]),
                self.system.input_variables["Income"].memberships["High"].calculate(inputs["Income"])
            ),
            "Applicant.Medium.1"
        ))         

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Asset"].memberships["Low"].calculate(inputs["Asset"]),
                self.system.input_variables["Income"].memberships["Very High"].calculate(inputs["Income"])
            ),
            "Applicant.High.1"
        ))     

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Asset"].memberships["Medium"].calculate(inputs["Asset"]),
                self.system.input_variables["Income"].memberships["Low"].calculate(inputs["Income"])
            ),
            "Applicant.Low.3"
        )) 

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Asset"].memberships["Medium"].calculate(inputs["Asset"]),
                self.system.input_variables["Income"].memberships["Medium"].calculate(inputs["Income"])
            ),
            "Applicant.Medium.2"
        )) 

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Asset"].memberships["Medium"].calculate(inputs["Asset"]),
                self.system.input_variables["Income"].memberships["High"].calculate(inputs["Income"])
            ),
            "Applicant.High.2"
        ))         

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Asset"].memberships["Medium"].calculate(inputs["Asset"]),
                self.system.input_variables["Income"].memberships["Very High"].calculate(inputs["Income"])
            ),
            "Applicant.High.3"
        ))         

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Asset"].memberships["High"].calculate(inputs["Asset"]),
                self.system.input_variables["Income"].memberships["Low"].calculate(inputs["Income"])
            ),
            "Applicant.Medium.3"
        )) 

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Asset"].memberships["High"].calculate(inputs["Asset"]),
                self.system.input_variables["Income"].memberships["Medium"].calculate(inputs["Income"])
            ),
            "Applicant.Medium.4"
        )) 

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Asset"].memberships["High"].calculate(inputs["Asset"]),
                self.system.input_variables["Income"].memberships["High"].calculate(inputs["Income"])
            ),
            "Applicant.High.4"
        ))         

        # 
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Asset"].memberships["High"].calculate(inputs["Asset"]),
                self.system.input_variables["Income"].memberships["Very High"].calculate(inputs["Income"])
            ),
            "Applicant.High.5"
        ))         

        """ CREDIT EVALUATION RULES """

        #
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Income"].memberships["Low"].calculate(inputs["Income"]),
                self.system.input_variables["Interest"].memberships["Low"].calculate(inputs["Interest"])
            ),
            "Credit.Very Low.1"
        ))

        #
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Income"].memberships["Low"].calculate(inputs["Income"]),
                self.system.input_variables["Interest"].memberships["High"].calculate(inputs["Interest"])
            ),
            "Credit.Very Low.2"
        ))

        #
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.input_variables["Income"].memberships["Medium"].calculate(inputs["Income"]),
                self.system.input_variables["Interest"].memberships["High"].calculate(inputs["Interest"])
            ),
            "Credit.Low.1"
        ))
        
        #
        self.system.add_rule(FuzzyRule(#SORUN
            lambda inputs : 
                self.system.output_variables["Applicant"].memberships["Low"].calculate(inputs["Applicant"]),
            "Credit.Very Low.3"
        ), 1)              

        #
        self.system.add_rule(FuzzyRule(#Sorun
            lambda inputs : 
                self.system.output_variables["House"].memberships["Very Low"].calculate(inputs["House"]),
            "Credit.Very Low.4"
        ), 1) 

        #
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.output_variables["Applicant"].memberships["Medium"].calculate(inputs["Applicant"]),
                self.system.output_variables["House"].memberships["Very Low"].calculate(inputs["House"]),
            ),
            "Credit.Low.2"
        ), 1)         

        #
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.output_variables["Applicant"].memberships["Medium"].calculate(inputs["Applicant"]),
                self.system.output_variables["House"].memberships["Low"].calculate(inputs["House"]),
            ),
            "Credit.Low.3"
        ), 1)  

        #
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.output_variables["Applicant"].memberships["Medium"].calculate(inputs["Applicant"]),
                self.system.output_variables["House"].memberships["Medium"].calculate(inputs["House"]),
            ),
            "Credit.Medium.1"
        ), 1)  

        #
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.output_variables["Applicant"].memberships["Medium"].calculate(inputs["Applicant"]),
                self.system.output_variables["House"].memberships["High"].calculate(inputs["House"]),
            ),
            "Credit.High.1"
        ), 1)                  

        #
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.output_variables["Applicant"].memberships["Medium"].calculate(inputs["Applicant"]),
                self.system.output_variables["House"].memberships["Very High"].calculate(inputs["House"]),
            ),
            "Credit.High.2"
        ), 1)          


        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.output_variables["Applicant"].memberships["High"].calculate(inputs["Applicant"]),
                self.system.output_variables["House"].memberships["Very Low"].calculate(inputs["House"]),
            ),
            "Credit.Low.4"
        ), 1)         

        #
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.output_variables["Applicant"].memberships["High"].calculate(inputs["Applicant"]),
                self.system.output_variables["House"].memberships["Low"].calculate(inputs["House"]),
            ),
            "Credit.Medium.2"
        ), 1)  

        #
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.output_variables["Applicant"].memberships["High"].calculate(inputs["Applicant"]),
                self.system.output_variables["House"].memberships["Medium"].calculate(inputs["House"]),
            ),
            "Credit.High.3"
        ), 1)  

        #
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.output_variables["Applicant"].memberships["High"].calculate(inputs["Applicant"]),
                self.system.output_variables["House"].memberships["High"].calculate(inputs["House"]),
            ),
            "Credit.High.4"
        ), 1)                  

        #
        self.system.add_rule(FuzzyRule(
            lambda inputs : min(
                self.system.output_variables["Applicant"].memberships["High"].calculate(inputs["Applicant"]),
                self.system.output_variables["House"].memberships["Very High"].calculate(inputs["House"]),
            ),
            "Credit.Very High.1"
        ), 1)


    """ Creates the system """
    def CreateControlSystem(self):
        
        self.CreateInputVariables()
        self.CreateOutputVariables()
        self.CreateRules()

    """Runs the system and returns the output"""
    def RunSimulation(self, inputs):    

        return self.system.evaluate(inputs)

    """ Returns the output values and related classes """
    def GetOutputDegrees(self, output):

        output_degrees = {}

        for var_name, var in self.system.output_variables.items():
            output_degrees[var_name] = var.calculate_membership_degrees(output[var_name])
        
        return output_degrees

    """ Returns the input values and classes as dict """
    def GetInputDegrees(self, inputs):
        
        input_degrees = {}
        for var_name, var in self.system.input_variables.items():
            input_degrees[var_name] = var.calculate_membership_degrees(inputs[var_name])
        
        return input_degrees

    """Returns the dominant classes and values of output variables """
    def get_Dominant_Category_Value(self, outputs):

        dominant_categories = {}

        for var_name, output_value in outputs.items():
            max_value = output_value
            dominant_category = max(self.system.output_variables[var_name].memberships.items(), 
                                    key=lambda x: x[1].calculate(max_value))

            dominant_categories[var_name] = dominant_category[0]
        
        return dominant_categories
    

def getInputMemberships():

    fuzzy_system = FuzzyControlSystem()
    marketvalue, location, asset, income, interest = fuzzy_system.CreateInputVariables()

    return marketvalue, location, asset, income, interest

def getOutputMemberships():
    
    fuzzy_system = FuzzyControlSystem()
    house, applicant, credit = fuzzy_system.CreateOutputVariables()

    return house, applicant, credit


""" BASE USAGE """    

def main(inputs):

    fuzzy_system = FuzzyControlSystem()
    fuzzy_system.CreateControlSystem()


    output = fuzzy_system.RunSimulation(inputs[0])

    output_degrees = fuzzy_system.GetOutputDegrees(output)
    
    input_degrees = fuzzy_system.GetInputDegrees(inputs[0])

    dominant_categories = fuzzy_system.get_Dominant_Category_Value(output)


    return output, output_degrees, input_degrees, dominant_categories

