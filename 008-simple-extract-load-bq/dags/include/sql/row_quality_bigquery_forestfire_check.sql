SELECT
    COUNT(*) AS total_rows
FROM `{{ var.value.gcp_project_id }}.astronomer.forestfires`
WHERE
    id = @id