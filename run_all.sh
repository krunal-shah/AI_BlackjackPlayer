#!/bin/bash
mkdir -p output_km
./run.sh 0.103 
echo "Running ./output_km/1.txt"
mv "Policy.txt" "./output_km/1.txt"
diff ./output_km/1.txt ./output/1.txt
./run.sh 0.235 
echo "Running ./output_km/2.txt"
mv "Policy.txt" "./output_km/2.txt"
diff ./output_km/2.txt ./output/2.txt
./run.sh 0.001 
echo "Running ./output_km/3.txt"
mv "Policy.txt" "./output_km/3.txt"
diff ./output_km/3.txt ./output/3.txt
./run.sh 0.023 
echo "Running ./output_km/4.txt"
mv "Policy.txt" "./output_km/4.txt"
diff ./output_km/4.txt ./output/4.txt
./run.sh 0.345 
echo "Running ./output_km/5.txt"
mv "Policy.txt" "./output_km/5.txt"
diff ./output_km/5.txt ./output/5.txt
./run.sh 0.459 
echo "Running ./output_km/6.txt"
mv "Policy.txt" "./output_km/6.txt"
diff ./output_km/6.txt ./output/6.txt
./run.sh 0.467 
echo "Running ./output_km/7.txt"
mv "Policy.txt" "./output_km/7.txt"
diff ./output_km/7.txt ./output/7.txt
./run.sh 0.266 
echo "Running ./output_km/8.txt"
mv "Policy.txt" "./output_km/8.txt"
diff ./output_km/8.txt ./output/8.txt
./run.sh 0.003 
echo "Running ./output_km/9.txt"
mv "Policy.txt" "./output_km/9.txt"
diff ./output_km/9.txt ./output/9.txt
./run.sh 0.111 
echo "Running ./output_km/10.txt"
mv "Policy.txt" "./output_km/10.txt"
diff ./output_km/10.txt ./output/10.txt
./run.sh 0.456 
echo "Running ./output_km/11.txt"
mv "Policy.txt" "./output_km/11.txt"
diff ./output_km/11.txt ./output/11.txt
./run.sh 0.333 
echo "Running ./output_km/12.txt"
mv "Policy.txt" "./output_km/12.txt"
diff ./output_km/12.txt ./output/12.txt
./run.sh 0.222 
echo "Running ./output_km/13.txt"
mv "Policy.txt" "./output_km/13.txt"
diff ./output_km/13.txt ./output/13.txt
./run.sh 0.239 
echo "Running ./output_km/14.txt"
mv "Policy.txt" "./output_km/14.txt"
diff ./output_km/14.txt ./output/14.txt
./run.sh 0.016 
echo "Running ./output_km/15.txt"
mv "Policy.txt" "./output_km/15.txt"
diff ./output_km/15.txt ./output/15.txt
