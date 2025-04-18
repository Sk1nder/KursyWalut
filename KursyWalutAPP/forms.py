from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField, DateField
from wtforms.validators import NumberRange


from KursyWalutAPP.utils import currRateMid
from KursyWalutAPP.utils import currCodesList


class Form(FlaskForm):
    firstCurrIndex = SelectField('First currency Index', choices=["PLN"], default="PLN")
    secondCurrIndex = SelectField('Second currency Index', choices=currCodesList, default="EUR - euro")
    firstCurr = FloatField("First currency value", default=1, validators=[NumberRange(min=0)])
    secondCurr = FloatField("Second currency value", default=round(1/currRateMid("eur"), 4), validators=[NumberRange(min=0)])


