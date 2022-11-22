select *
from cbe.entities as e
inner join cbe.entities_persons as ep on ep.entity_id = e.id
inner join cbe.persons as p on p.id = ep.person_id
left join cbe.entities_entities as ee on ee.person_id = ep.person_id; 

select (last_name, first_name)
from cbe.entities as e
inner join cbe.entities_persons as ep on ep.entity_id = e.id
inner join cbe.persons as p on p.id = ep.person_id;