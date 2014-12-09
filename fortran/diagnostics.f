! Subroutine Grad
! Calculated the gradient of a scalar field on an irregular grid

      SUBROUTINE grad(field,altitude,dy,dx,nz,ny,nx

      IMPLICIT NONE

      INTEGER nz,ny,nx
              ! Grid Dimensions
      REAL    field(nz,ny,nx),                                          &
              ! Input Field
              altitude(nz,ny,nx)                                        &
              ! Height at each gridpoint


CF2PY      INTEGER, INTENT(HIDE)    :: nz
CF2PY      INTEGER, INTENT(HIDE)    :: ny
CF2PY      INTEGER, INTENT(HIDE)    :: nx              
CF2PY      REAL, INTENT(IN)         :: field(nz,ny,nx)
CF2PY      REAL, INTENT(IN)         :: altitude(nz,ny,nx)
CF2PY      REAL, INTENT(IN)         :: 

      d_dz = 0.0
      d_dy = 0.0
      d_dx = 0.0
      
      ! Loop over all point apart from boundaries
      DO k = 2,nz-1
        DO j = 2,ny-1
          DO i = 2,nx-1
            d_dz = field(k-1,j,i
            d_dy = (field(k,j+1,i) - field(k,j-1,i))
            d_dx = (field(k,j,i+1) - field(k,j,i+1))
