import sympy

# Pretty printing
sympy.init_printing()

class Metric:
    """
    Input arguments:
        g:
            sympy.Matrix
            Contains the covariant components of the metric tensor

        coordinates:
            list/array of sympy.Symbol
            Contains the coordinates in which the metric tensor is expressed

    The class has methods for:
        - differentiating the metric tensor with respect to given coordinate
        - computing Christoffel symbols of the metric
        - computing the right-hand-side of a given component of the geodesic equation
    """

    def __init__(self, g, coordinates):
        self.g = g                      # The covariant components of the metric tensor
        self.g_inv = self.g.inv()       # The contravariant ---------||----------------
        self.coordinates = coordinates  # The coordinates in which we express the metric

        self.dim = len(self.coordinates)  # Dimension of the spacetime in question (will assume 4-dim in other parts of the code. That should be generalized)

        # Sympy variables representing the components of the four-velocity of a particle
        # u0 is dx^0/dlambda, u1 is dx^1/dlambda etc.
        # (have explicitly here assumed a (3 + 1) dimensional spacetime, which is not ideal...)
        u0, u1, u2, u3 = sympy.symbols("u0, u1, u2, u3")
        self.velocities = [u0, u1, u2, u3]

        # List containing the right-hand-side (rhs) of each component of the geodesic equation
        self.geodesic_rhs = [self.compute_geodesic_rhs(i) for i in range(self.dim)]

    def deriv(self, mu, nu, rho):
        """
        Differentiates the metric tensor component g_(mu nu) with respect to coordinate rho (corresponding to self.coordinates[rho])
        """
        return sympy.diff(self.g[mu, nu], self.coordinates[rho])

    def compute_christoffel(self, mu, rho, sigma):
        """
        Computes the Christoffel symbol Gamma^(mu)_(rho sigma) by calling the function self.deriv()
        """
        result = sympy.Float(0)

        for nu in range(self.dim):
            result += 1.0/2.0*self.g_inv[mu, nu]*(self.deriv(nu, rho, sigma) + self.deriv(nu, sigma, rho) - self.deriv(rho, sigma, nu))

        return result

    def compute_geodesic_rhs(self, mu):
        """
        Computes the mu-th component of the geodesic equation, which comes down to calculating the Christoffel symbols
        """
        result = sympy.Float(0)

        for rho in range(self.dim):
            for sigma in range(self.dim):
                result -= self.compute_christoffel(mu, rho, sigma)*self.velocities[rho]*self.velocities[sigma]

        return result

def getMetric(name):
    """
    Takes as input argument the name of a metric, either "kerr" or "schwarzschild"
    and returns a Metric-object containing the corresponding metric. Also returns
    a list containing all the variables entering the metric, as sympy.symbols.
    """
    t, r, theta, phi, M, a = sympy.symbols("t, r, theta, phi, M, a")

    coordinates = [t, r, theta, phi]

    sigma = r**2 + a**2*sympy.cos(theta)**2
    delta = r**2 - 2*M*r + a**2

    # Kerr metric
    g = sympy.Matrix([[-(1 - 2*M*r/sigma), 0, 0, -2*a*M*r/sigma*sympy.sin(theta)**2],
                      [0, sigma/delta, 0, 0], [0, 0, sigma, 0],
                      [-2*a*M*r/sigma*sympy.sin(theta)**2, 0, 0,
                      (r**2 + a**2 + 2*M*r*a**2/sigma*sympy.sin(theta)**2)*sympy.sin(theta)**2]])

    kerr = Metric(g, coordinates)

    # Schwarzschild metric
    g = sympy.Matrix([[-(1 - 2*M/r), 0, 0, 0], [0, (1 - 2*M/r)**(-1), 0, 0], [0, 0, r**2, 0], [0, 0, 0, r**2*sympy.sin(theta)**2]])

    schwarzschild = Metric(g, coordinates)

    metrics = {"kerr": [kerr, [t, r, theta, phi, M, a]], "schwarzschild": [schwarzschild, [t, r, theta, phi, M]]}
    return metrics[name]
