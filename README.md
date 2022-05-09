# ASTRO-5
A coded experiment in the ISS to evaluate the state of health of forest masses near urban areas on Earth, under the Astro Pi project: Mission Space Lab.
1. Participants:
The team is made up of five first-year high school students:
   - Diego Manuel Mariscal Jiménez.
   - Gonzalo Pérez Ribes.
   - Rocío Santana Moya.
   - Mario Torres Danta.
   - Daniel Wagner López.
   - Mentor: David Pamos Ortega. Dpto. de Física y Química. IES Levante. Algeciras. Spain

2. Objective:
The main objective of this experiment is to evaluate the quality of life in different areas of the planet, estimating the albedo, the NDVI of forest areas and measuring the magnetic field. We want to check possible correlations between these parameters.

3. Method for achieving the objective:
The code measures the magnetic field, using the magnetometer, every 12 seconds, and takes visible pictures whenever it is daylight and also every 12 seconds, in order to optimize the storage space. We will also use NDVI data, through EO Browser, from the forest areas through which the ISS passes during our experiment. The selected visible photographs will be treated later using another code that estimates the albedo, based on the percentage of pixels that contain sea, vegetation or land. Considering the chosen resolution, (2592, 1944), and the frequency with which the photographs will be taken, as well as the fact that it will only take them during daylight, we estimate that the storage space does not exceed 1500 Mb.

4. Expected results:
Depending on the photographs that we get, we suppose that the areas that have an albedo close to the average value of the Earth, will also have a healthy NDVI value, in the case of aquatic areas close to healthy vegetation. We do not expect, in principle, a correlation between these parameters and the value of the magnetic field in these areas.
