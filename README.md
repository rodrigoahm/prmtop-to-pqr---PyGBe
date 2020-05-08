# prmtop-to-pqr---PyGBe

prmtop to pqr.ipynb transformar una o más moléculas en formato .prmtop y .crd a .pqr. 
- Dentro del notebook se pueden cambiar los directorios así como los parámetros. 
- También es posiblie generar una recopilación de los resultados entregados por PyGBe, pero esto sólo se puede hacer una vez, ya que se cambia el documento de .log a .revisado

En la carpeta de los resultados se encuentran los .ipynb energy_plots y new_implicit_data.
Para generar un documento con resultados comparables en energy_plots, es necesario utilizar new_implicit_data, la cual ordena los resultados acorde al explicit_data a comparar, además genera un documento con las moléculas y sus respectivos números de átomos y volumenes.




Se utilizan las moléculas utilidas por David Mobley, para evitar problemas con la lectura de los resultados en Energy_plots.ipynb hay que modificar los siguientes nombres:
- N_methyl_N__222_trifluoroethyl__aniline --> N_methyl_N_222_trifluoroethyl_aniline
- bis_2_chloroethyl__ether --> bis_2_chloroethyl_ether
- m_bis_trifluoromethyl__benzene --> m_bis_trifluoromethyl_benzene

Dentro de la misma base de datos, MSMS tiene problemas para generar las mallas de las moléculas:
- ammonia 
- hydrogen_sulfide
