test.User.find( {} ).count()

test.User.find ( {Location: "New York"} ).count()

test.Item.find( {Category : {$eq: 4} } ).count()

test.Item.find().sort({Currently:-1}).limit(1)

test.Item.find( {User : {Rating :  {$gt: 1000} } } ).count()

test.Item.find( {Category : {Currently : {$gte : 100}}} ).count()

