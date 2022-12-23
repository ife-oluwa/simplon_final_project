from flask import (
    Blueprint, flash, g, redirect, request, render_template, url_for, session
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from operator import itemgetter
import joblib
from flaskr.auth import login_required
from flaskr.db import get_db
import pandas as pd


bp = Blueprint('predict', __name__)

model = joblib.load(open('model\BRidge_model.sav', 'rb'))

format = "%d-%m-%y, %H:%M:%S"


@bp.route('/history')
@login_required
def history():
    db = get_db()
    user_id = session.get('user_id')

    results = db.execute(
        '''SELECT p.id as id, created, MasVnrArea, GarAreaPerCar, TotalHouseSF, TotalFullBath, InitHouseAge, RemodHouseAge, GarageAge, TotalPorchSF, Overall_Qual, Overall_Cond, SalePrice
        FROM predictions p JOIN user u ON p.user_id = u.id
        WHERE u.id = ?
        ORDER BY created DESC''', (user_id,)
    ).fetchall()
    results_list = []
    for result in results:
        results_list.append(dict(result))
    sorted_list = sorted(results_list, key=itemgetter('id'))

    if len(results) > 0:
        return render_template('predict/history.html', result=sorted_list, has_results='Yes')
    else:
        return render_template('predict/history.html', has_results='No')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    X_predict = {}
    pred = 0
    user_id = session.get('user_id')
    if request.method == 'POST':

        MasVnrArea = float(request.form['MasVnrArea'])
        GarAreaPerCar = float(request.form['GarAreaPerCar'])
        TotalHouseSF = float(request.form['TotalHouseSF'])
        TotalFullBath = float(request.form['TotalFullBath'])
        InitHouseAge = int(request.form['InitHouseAge'])
        RemodHouseAge = float(request.form['RemodHouseAge'])
        GarageAge = int(request.form['GarageAge'])
        TotalPorchSF = float(request.form['TotalPorchSF'])
        Overall_Qual = int(request.form['Overall_Qual'])
        Overall_Cond = int(request.form['Overall_Cond'])
        AvgQualCond = (Overall_Cond + Overall_Qual)/2

        X_predict['MasVnrArea'] = MasVnrArea
        X_predict['GarAreaPerCar'] = GarAreaPerCar
        X_predict['TotalHouseSF'] = TotalHouseSF
        X_predict['TotalFullBath'] = TotalFullBath
        X_predict['InitHouseAge'] = InitHouseAge
        X_predict['RemodHouseAge'] = RemodHouseAge
        if float(X_predict['RemodHouseAge']) > 0:
            X_predict['IsRemod'] = 1
        else:
            X_predict['IsRemod'] = 0
        X_predict['GarageAge'] = GarageAge
        X_predict['TotalPorchSF'] = TotalPorchSF
        X_predict['AvgQualCond'] = AvgQualCond

        isRemod = X_predict['IsRemod']

        pred = float(model.predict(pd.DataFrame(X_predict, index=[0])))
        db_val = [g.user['id'], MasVnrArea, GarAreaPerCar, TotalHouseSF, TotalFullBath,
                  InitHouseAge, RemodHouseAge, isRemod, GarageAge, TotalPorchSF, Overall_Qual, Overall_Cond]
        db_val.append(pred)
        val_tuple = tuple(db_val)
        print(f"{pred:.2f}")
        # rewrite to have the data and prediction committed to db.
        db = get_db()

        error = None

        if len(db_val) != 13:
            error = 'Missing variables. Please check.'
        if error is None:
            try:
                db.execute(
                    """INSERT INTO predictions ('user_id','MasVnrArea', 'GarAreaPerCar', 'TotalHouseSF',
                                                'TotalFullBath', 'InitHouseAge', 'IsRemod', 'RemodHouseAge',
                                                'GarageAge', 'TotalPorchSF', 'Overall_Qual',
                                                'Overall_Cond', 'SalePrice')
                                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
                        user_id, MasVnrArea, GarAreaPerCar, TotalHouseSF, TotalFullBath, InitHouseAge,
                        isRemod, RemodHouseAge, GarageAge, TotalPorchSF, Overall_Qual, Overall_Cond, pred
                    )
                )
                db.commit()
            except db.IntegrityError as e:
                print(f'Error: {e}')
        flash(error)
    return render_template('predict/index.html', data=f"${float(pred):.2f}")


def get_profile(user_id, check_user=True):
    profile = get_db().execute(
        '''
            SELECT *
            FROM user
            WHERE id = ?
        ''', (user_id,)).fetchone()
    get_db().commit()
    if profile is None:
        abort(404, f"Profile id {user_id} doesn't exist")
    if check_user and profile['id'] != g.user['id']:
        abort(403)
    return profile


@ bp.route('/update', methods=['GET', 'POST'])
@ login_required
def update():
    user_id = session.get('user_id')
    db = get_db()
    profile = get_profile(user_id)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass1']
        pass2 = request.form['pass2']

        error = None

        if password != pass2:
            error = 'Please make sure passwords are the same.'
        if error is None:
            db.execute(
                """
                    UPDATE user SET email = ?, password = ? WHERE id = ?
                """, (email, generate_password_hash(password), user_id)
            )
            db.commit()
            return redirect(url_for('predict.index'))
        else:
            flash(error)
    return render_template('predict/profile.html', profile=dict(profile))
