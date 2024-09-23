INSERT INTO `{{ var.value.gcp_project_id }}.astronomer.forestfires`
  (id, y, month, day, ffmc, dmc, dc, isi, temp, rh, wind, rain, area)
VALUES
  (1, 1, 'jan', 'mon', 85.4, 26.2, 94.3, 5.1, 22.1, 45, 4.5, 0.0, 0.3),
  (2, 0, 'feb', 'tue', 90.2, 35.4, 99.1, 7.0, 18.3, 35, 3.2, 0.2, 1.1);