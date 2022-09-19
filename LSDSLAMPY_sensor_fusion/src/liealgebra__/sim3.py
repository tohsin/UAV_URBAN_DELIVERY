import sophus as sp
import numpy as np

class SIM3():
    dof = 3
    dim = 3
    RotationType = sp.SO3()
    def __init__(self, rot = None, trans = None) -> None:
        self.rot = rot
        self.trans = trans
    @classmethod
    def exp(cls, xi):
        rho = xi[0:3]
        phi = xi[3:6]
        sigma = xi[6:7]
        exp_sigma = np.exp(sigma)
        exp_so3 = sp.SO3.exp(phi)
        
        return cls(np.dot(exp_sigma, exp_so3) , np.dot(cls.left_jacobian(phi,sigma), rho) )
    @classmethod
    def wedge(cls, phi):
      
        if phi.shape[1] != cls.dof:
            raise ValueError(
                "phi must have shape ({},) or (N,{})".format(cls.dof, cls.dof))

        Phi = np.zeros([phi.shape[0], cls.dim, cls.dim])
        Phi[:, 0, 1] = -phi[:, 2]
        Phi[:, 1, 0] = phi[:, 2]
        Phi[:, 0, 2] = phi[:, 1]
        Phi[:, 2, 0] = -phi[:, 1]
        Phi[:, 1, 2] = -phi[:, 0]
        Phi[:, 2, 1] = phi[:, 0]
        return np.squeeze(Phi)
    @classmethod
    def left_jacobian(cls, phi, sigma):
        # phi = theta * a
        """
        sigma - scale
        phi - rotation
        rho - translation
        """
        theta_ =  np.linalg.norm(phi)
        a = phi / theta_
        sig_thet = (sigma ** 2 + theta_ **2)

        if np.isclose(theta_, 0.):
            return np.identity(cls.dof) + 0.5 * cls.wedge(phi)

        exp_sigma = np.exp(sigma)
        s = np.sin(theta_)
        c = np.cos(theta_)
        return ( (exp_sigma - 1)/sigma) * np.identity(cls.dof)  + \
           ( (( (sigma * exp_sigma * s) + ((1 - (exp_sigma * c) * theta_) ))) / sig_thet) *  cls.wedge(a) + \
           ( ((exp_sigma -1)/sigma)  -   (((((exp_sigma * c) - 1) * sigma) + ((exp_sigma * s) * theta_) )/ sig_thet) ) * np.outer(a, a)

        