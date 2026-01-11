from flask import Blueprint, jsonify, request
from config import db
from app.models import Hero, Power, HeroPower

bp = Blueprint('routes', __name__)

@bp.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([{'id': h.id, 'name': h.name, 'super_name': h.super_name} for h in heroes])

@bp.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404

    hero_powers = []
    for hp in hero.hero_powers:
        hero_powers.append({
            'id': hp.id,
            'hero_id': hp.hero_id,
            'power_id': hp.power_id,
            'strength': hp.strength,
            'power': {'id': hp.power.id, 'name': hp.power.name, 'description': hp.power.description}
        })

    return jsonify({'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'hero_powers': hero_powers})


@bp.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'description': p.description} for p in powers])

@bp.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    return jsonify({'id': power.id, 'name': power.name, 'description': power.description})

@bp.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    data = request.get_json()
    description = data.get('description')
    if not description or len(description) < 20:
        return jsonify({'errors': ['description must be at least 20 characters']}), 400

    power.description = description
    db.session.commit()
    return jsonify({'id': power.id, 'name': power.name, 'description': power.description})


@bp.route('/hero_powers', methods=['POST'])
def add_hero_power():
    data = request.get_json()
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    if strength not in ['Strong', 'Weak', 'Average']:
        return jsonify({'errors': ['strength must be Strong, Weak, or Average']}), 400

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
    if not hero or not power:
        return jsonify({'errors': ['Invalid hero_id or power_id']}), 400

    hp = HeroPower(hero_id=hero.id, power_id=power.id, strength=strength)
    db.session.add(hp)
    db.session.commit()

    return jsonify({
        'id': hp.id,
        'hero_id': hp.hero_id,
        'power_id': hp.power_id,
        'strength': hp.strength,
        'hero': {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name},
        'power': {'id': power.id, 'name': power.name, 'description': power.description}
    })
