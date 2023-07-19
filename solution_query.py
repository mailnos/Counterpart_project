from rater_example import rater

json_input = {'Asset Size': 1200000, 'Limit': 5000000, 'Retention': 1000000,'Industry': 'Hazard Group 2'}
result = rater(json_input)
print(result)

json_input = {'Asset Size': 0, 'Limit': 5000000, 'Retention': 1000000,'Industry': 'Hazard Group 2'}
result = rater(json_input)
print(result)

json_input = {'Asset Size': 50, 'Limit': 5000000, 'Retention': 1000000,'Industry': 'Hazard Group 2'}
result = rater(json_input)
print(result)

 