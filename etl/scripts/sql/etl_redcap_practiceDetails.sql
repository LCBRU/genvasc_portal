SELECT
      p.practice_name
    , p.practice_code
FROM (
    SELECT
         pn.value AS practice_name
       , pc.value AS practice_code
       , i.value AS initiated
    FROM	redcap_data pn
    JOIN	redcap_data pc ON
                pc.record = pn.record
			  AND pc.project_id = pn.project_id
			  AND pc.field_name = 'practice_code'
	JOIN	redcap_data i ON
	            i.record = pn.record
			  AND i.project_id = pn.project_id
			  AND i.field_name = 'genvasc_initiated'
	WHERE
	        pn.field_name = 'practice_name'
		 AND pn.project_id = 41
	GROUP BY pn.record
) p
WHERE p.initiated = 1