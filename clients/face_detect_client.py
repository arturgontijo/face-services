import grpc
import sys

import services.grpc.face_detect_pb2
import services.grpc.face_detect_pb2_grpc
from services.grpc.face_common_pb2 import ImageRGB

def read_in_chunks(filename, chunk_size=1024*64):
    with open(filename, 'rb') as infile:
        while True:
            chunk = infile.read(chunk_size)
            if chunk:
                yield ImageRGB(content=chunk)
            else:
                # The chunk was empty, which means we're at the end
                # of the file
                return

def find_faces(stub, image_fn):
    img_iterator = read_in_chunks(image_fn)
    return stub.FindFace(img_iterator)

def run(image_fn):
    channel = grpc.insecure_channel('localhost:50051')
    stub = services.grpc.face_detect_pb2_grpc.FaceDetectStub(channel)
    print("-------------- FindFaces --------------")
    faces = find_faces(stub, image_fn)
    print(faces)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print("Usage: python %s image.jpg" % __file__)