import g2o

pose = g2o.Sim3()
rot = pose.rotation()
pose_inv = pose.inverse()
rot_inv = pose_inv.rotation().R
print(rot_inv)
ref_pose = pose