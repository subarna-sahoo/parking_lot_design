# Parking Lot
## Build the Docker image
Let’s proceed to build the image with the command below:
`docker image build parking_lot_design`

# Run the container
After successfully building the image, the next step is to run an instance of the image. Here is how to perform this:
`docker run -p 8000:8000 -d parking_lot_design`

Pull the image from Docker
`docker pull subarnasahoo/parking_lot`