-- Manage leading zero padding in code.
insert into cbe.entities (id, enterprise_number)
values
    (default, '502465839' ),
    (default, '475697995' );

insert into cbe.persons (id, last_name, first_name)
values
    (default, 'Pirnay',	'Dimitri'),
    (default, 'Beazar',	'Guido');

insert into cbe.entities_persons (id, entity_id, person_id, function, start_date)
values
    (default, 1, 1, 'person_in_charge_of_daily_management', '2020-08-13'),
    (default, 1,	2,	'permanent_representative', '2020-08-13');

insert into cbe.entities_entities (id, represented_entity_id, representative_entity_id, function, person_id, start_date)
values(default, 1, 2, 'director', 2, '2020-08-13');