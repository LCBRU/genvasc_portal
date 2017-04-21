    SELECT
         LEFT(TRIM(pc.value), 6) AS code
       , TRIM(pn.value) AS name
       , CASE
           WHEN ccgname.name = 'LCCCG' THEN 'NHS Leicester City CCG'
           WHEN ccgname.name = 'ELCCG' THEN 'NHS East Leicestershire and Rutland CCG'
           WHEN ccgname.name = 'WLCCG' THEN 'NHS West Leicestershire CCG'
         END AS ccg_name
       , addr.value AS address
    FROM	redcap_data pn
    JOIN	redcap_data pc ON
                pc.record = pn.record
			  AND pc.project_id = pn.project_id
			  AND pc.field_name = 'practice_code'
	LEFT JOIN	redcap_data i ON
	            i.record = pn.record
			  AND i.project_id = pn.project_id
			  AND i.field_name = 'genvasc_initiated'
	LEFT JOIN	redcap_data ccg ON
	            ccg.record = pn.record
			  AND ccg.project_id = pn.project_id
			  AND ccg.field_name = 'ccg'
	LEFT JOIN LCBRU_Enums ccgname ON
	            ccgname.project_id = ccg.project_id
	        AND ccgname.field_name = ccg.field_name
	        AND ccgname.value = ccg.value
	LEFT JOIN	redcap_data addr ON
	            addr.record = pn.record
			  AND addr.project_id = pn.project_id
			  AND addr.field_name = 'practice_address'
	LEFT JOIN	redcap_data postcode ON
	            postcode.record = pn.record
			  AND postcode.project_id = pn.project_id
			  AND postcode.field_name = 'postcode'
	WHERE
	        pn.field_name = 'practice_name'
		 AND pn.project_id IN (38, 41)
	GROUP BY pn.record
