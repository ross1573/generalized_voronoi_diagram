# Generalized voronoi diagram  
A generalized voronoi diagram for python.  
Supports points, lines, polygons on generation.  
Description is available at https://doi.org/10.5391/IJFIS.2023.23.3.259  

-----  

### Requirments
~~~
python   
    - numpy  
    - matplotlib  
    - scipy  
    - rdp  
    - opencv-python  
    - numba  
    - tripy  
    - pyvisgraph  
~~~
-----  
  
### Path planning demo result
* non polygon lined(normal point based voronoi diagram)  
  <img src="./result/non_lined_result.png" width="430px" height="360px">

* non vertex deleted  
  <img src="./result/non_deleted_result.png" width="430px" height="360px">

* result of polygon based voronoi diagram  
  <img src="./result/non_optimized_result.png" width="430px" height="360px">

* result after optimization  
  <img src="./result/optimized_result.png" width="430px" height="360px">

* astar algorithm using optimized result  
  <img src="./result/astar_result.png" width="430px" height="360px">
-----  
  
### AirSim demo result
* reference detected result  
  <img src="./result/reference_bound_detect_result.png" width="430px" height="360px">

* polygon detected result  
  <img src="./result/polygon_detect_result.png" width="430px" height="360px">
  

https://user-images.githubusercontent.com/44907014/210353329-dc3fa047-4703-4018-9efe-72b539aa2ece.mp4

