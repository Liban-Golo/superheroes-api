from config import db
from app import create_app
from app.models import Hero, Power, HeroPower

app = create_app()

with app.app_context():
    HeroPower.query.delete()
    Hero.query.delete()
    Power.query.delete()
    db.session.commit()

    hero1 = Hero(name="Peter Parker", super_name="Spider-Man")
    hero2 = Hero(name="Bruce Wayne", super_name="Batman")
    hero3 = Hero(name="Clark Kent", super_name="Superman")
    db.session.add_all([hero1, hero2, hero3])
    db.session.commit()

    power1 = Power(name="Web-Slinging", description="Ability to swing through buildings using webs")
    power2 = Power(name="Martial Arts", description="Expert hand-to-hand combat skills")
    power3 = Power(name="Flight", description="Ability to fly at high speeds")
    power4 = Power(name="Super Strength", description="Extraordinary physical strength")
    db.session.add_all([power1, power2, power3, power4])
    db.session.commit()

    hp1 = HeroPower(hero_id=hero1.id, power_id=power1.id, strength="Strong")
    hp2 = HeroPower(hero_id=hero2.id, power_id=power2.id, strength="Strong")
    hp3 = HeroPower(hero_id=hero3.id, power_id=power3.id, strength="Strong")
    hp4 = HeroPower(hero_id=hero3.id, power_id=power4.id, strength="Strong")
    db.session.add_all([hp1, hp2, hp3, hp4])
    db.session.commit()

    print("Database seeded successfully!")
