from flask_app import app
from flask import render_template, redirect, session, request, flash, jsonify
from flask_app.models.sigh import Sigh
from flask_app.models.user import User

@app.route('/add/sigh')
def addSigh():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    loggedUser = User.get_user_by_id(data)
    return render_template('addSigh.html', loggedUser=loggedUser)


@app.route('/create/sigh', methods = ['POST'])
def createSigh():
    if 'user_id' not in session:
        return redirect('/')
    if not Sigh.validate_sigh(request.form):
        return redirect(request.referrer)
    data = {
        'location': request.form['location'],
        'whatHappened': request.form['whatHappened'],
        'date_of_setting': request.form['date_of_setting'],
        'of_sasquatches': request.form['of_sasquatches'],
        'user_id': session['user_id']
    }
    Sigh.create(data)
    return redirect('/')


@app.route('/sigh/<int:id>')
def viewSigh(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'sigh_id': id,
        'id': session['user_id']
    }
    sigh = Sigh.get_sigh_by_id(data)
    loggedUser = User.get_user_by_id(data)
    usersskeptic = Sigh.get_skeptics(data)
    skepticDetails = Sigh.get_skeptics_info(data)
    return render_template('sigh.html', sigh=sigh, loggedUser=loggedUser, usersskeptic=usersskeptic, skepticDetails=skepticDetails)


@app.route('/edit/sigh/<int:id>')
def editSigh(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'sigh_id': id,
        'id': session['user_id']
    }
    sigh = Sigh.get_sigh_by_id(data)
    if not sigh:
        return redirect('/')
    loggedUser = User.get_user_by_id(data)
    if sigh['user_id'] != loggedUser['id']:
        return redirect('/')

    return render_template('editSigh.html', sigh=sigh, loggedUser=loggedUser)


@app.route('/update/sigh/<int:id>', methods = ['POST'])
def updateSigh(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'sigh_id': id,
        'id': session['user_id']
    }
    sigh = Sigh.get_sigh_by_id(data)
    if not sigh:
        return redirect('/')
    loggedUser = User.get_user_by_id(data)
    if sigh['user_id'] != loggedUser['id']:
        return redirect('/')
    
    if len(request.form['location'])<1 or len(request.form['whatHappened'])<1 or len(request.form['date_of_setting'])<1:
        flash('All fields required', 'allRequired')
        return redirect(request.referrer)
    
    updateData = {
        'location': request.form['location'],
        'whatHappened': request.form['whatHappened'],
        'date_of_setting': request.form['date_of_setting'],
        'of_sasquatches': int(request.form['of_sasquatches']),
        'id': id
    }
    if not Sigh.validate_sigh(updateData):
        return redirect(request.referrer)
    Sigh.update_sigh(updateData)
    return redirect('/sigh/'+ str(id))
    
    

@app.route('/delete/sigh/<int:id>')
def deleteSigh(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'sigh_id': id,
        'id': session['user_id']
    }
    sigh = Sigh.get_sigh_by_id(data)
    if not sigh:
        return redirect('/')
    loggedUser = User.get_user_by_id(data)
    if loggedUser['id'] == sigh['user_id']:
        Sigh.delete_all_skeptics(data)
        Sigh.delete_sigh(data)
    return redirect('/')


@app.route('/skeptic/<int:id>')
def addSkeptic(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'sigh_id': id,
        'id': session['user_id']
    }
    usersskeptic = Sigh.get_skeptics(data)
    if session['user_id'] not in usersskeptic:
        Sigh.addSkeptic(data)
        return redirect(request.referrer)
    return redirect(request.referrer)


@app.route('/believe/<int:id>')
def believeIt(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'sigh_id': id,
        'id': session['user_id']
    }    
    Sigh.believeIt(data)
        
    return redirect(request.referrer)