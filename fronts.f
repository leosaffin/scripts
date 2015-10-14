!-----------------------------------------------------------------------!
!                          Grad 2D                                      !
!-----------------------------------------------------------------------!
      subroutine grad2d(x, dx, nx, ny, grad)
      ! Calculate the 2D vector-gradient given a scalar field x.

      implicit none

      integer ny, nx
              ! Grid Dimensions
      real    x(ny, nx),                                                 &
              ! 2D scalar field
     &        dx,                                                        &
              ! Grid spacing
     &        grad(ny, nx, 2)

CF2PY integer, intent(hide) :: nx
CF2PY integer, intent(hide) :: ny
CF2PY real, intent(in) :: dx
CF2PY real, intent(in) :: x(ny, nx)
CF2PY real, intent(out) :: grad(ny, nx, 2)

      ! Local Variables
      integer :: i,j
!-----------------------------------------------------------------------!
!                          START OF SUBROUTINE                          !
!-----------------------------------------------------------------------!
      grad = 0.0
      do j=2,ny-1
        do i=2,nx-1
          ! Calculate x-derivative
          grad(j, i, 1) = (x(j, i+1) - x(j, i-1)) / (2*dx)
          ! Calculate y-derivative
          grad(j, i, 2) = (x(j+1, i) - x(j-1, i)) / (2*dx)
        end do
      end do

      end subroutine grad2d

!-----------------------------------------------------------------------!
!                          Div 2D                                       !
!-----------------------------------------------------------------------!
      subroutine div2d(beta, D, dx, nx, ny, div)

      implicit none

      integer ny, nx
              ! Grid Dimensions
      real    beta(ny, nx), D(ny, nx),                                   &
     &        dx,                                                        &
     &        div(ny, nx)

CF2PY integer, intent(hide) :: nx
CF2PY integer, intent(hide) :: ny
CF2PY real, intent(in) :: beta(ny, nx)
CF2PY real, intent(in) :: D(ny, nx)
CF2PY real, intent(in) :: dx
CF2PY real, intent(in) :: x(ny, nx)
CF2PY real, intent(out) :: div(ny, nx)

      ! Local Variables
      integer :: i,j
      real :: d1, d2, d3, d4
!-----------------------------------------------------------------------!
!                          START OF SUBROUTINE                          !
!-----------------------------------------------------------------------!
      div = 0.0
      do j=2,ny-1
        do i=2,nx-1
          ! Resolve the outer vectors on to the middle point
          d1 = D(j-1,i)*(cos(beta(j-1,i))*cos(beta(j,i)) +               &
     &                   sin(beta(j-1,i))*sin(beta(j,i)))

          d2 = D(j,i-1)*(cos(beta(j,i-1))*cos(beta(j,i)) +               &
     &                   sin(beta(j,i-1))*sin(beta(j,i)))

          d3 = D(j,i+1)*(cos(beta(j,i+1))*cos(beta(j,i)) +               &
     &                   sin(beta(j,i+1))*sin(beta(j,i)))

          d4 = D(j+1,i)*(cos(beta(j+1,i))*cos(beta(j,i)) +               &
     &                   sin(beta(j+1,i))*sin(beta(j,i)))

          ! Calculate the divegence using first order finite
          ! differencing
          div(j,i) = (d4 - d1 + d3 - d2)/2*dx
        end do
      end do

      end subroutine div2d

!-----------------------------------------------------------------------!
!                             Axis                                      !
!-----------------------------------------------------------------------!
      subroutine axis(x, ny, nx, beta_res, D_res)
      ! Calculate the mean axis from the vector quantity x following
      ! the graphical method in A2.2 in Hewson (1998) for n=5.

      implicit none

      integer ny, nx
              ! Grid Dimensions
      real    x(ny, nx, 2), beta_res(ny,nx), D_res(ny,nx)

CF2PY integer, intent(hide) :: nx
CF2PY integer, intent(hide) :: ny
CF2PY real, intent(in) :: x(ny, nx)
CF2PY real, intent(out) :: beta_res(ny, nx)
CF2PY real, intent(out) :: D_res(ny, nx)

      ! Local Variables
      integer :: i,j
      real :: beta, D, new_x(ny,nx,2), xpos(ny,nx), ypos(ny,nx), x_res, &
     &        y_res
      ! Declare local constant Pi
      real, parameter :: pi = 3.1415927
!-----------------------------------------------------------------------!
!                          START OF SUBROUTINE                          !
!-----------------------------------------------------------------------!

      new_x = x
      do j=1,ny
        do i=1,nx
          ! Turn the vector into an axis between 0-180 degrees
          if(x(j,i,2).lt.0) then
            new_x(j,i,1) = -x(j,i,1)
            new_x(j,i,2) = -x(j,i,2)
          end if
          ! Calculate the angle the vector makes with the x-axis
          beta = atan2(new_x(j,i,2), new_x(j,i,1))

          ! Calculate the magnitude of the vector
          D = sqrt(new_x(j,i,1)**2 + new_x(j,i,2)**2)

          ! Calculate the new position of the vector with a doubled
          ! angle
          xpos(j,i) = D*cos(2*beta)
          ypos(j,i) = D*sin(2*beta)
        end do
      end do

      do j=1,ny
        do i=1,nx
          ! Calculate the resultant vector of the five points
          x_res = xpos(j+1,i) + xpos(j,i+1) + xpos(j,i) +               &
     &            xpos(j-1,i) + xpos(j,i-1)
          y_res = ypos(j+1,i) + ypos(j,i+1) + ypos(j,i) +               &
     &            ypos(j-1,i) + ypos(j,i-1)

          ! Calculate the five point mean angle
          beta_res(j,i) = atan2(x_res, y_res)/2.0

          ! Convert angles to between 0-180 degrees
          if (beta_res(j,i).lt.0) then
            beta_res(j,i) = beta_res(j,i) + pi/2.0
          end if

          ! Calculate the five point mean magnitude
          D_res(j,i) = sqrt(x_res**2 + y_res**2)/5.0
        end do
      end do

      end subroutine axis

!-----------------------------------------------------------------------!
!                          5 Point Ave                                  !
!-----------------------------------------------------------------------!
      subroutine fivepointave(x, dx, nx, ny, ave)

      implicit none

      integer ny, nx
              ! Grid Dimensions
      real    x(ny, nx),                                                 &
              ! 2d array
     &        dx,                                                        &

     &        ave(ny, nx)

CF2PY integer, intent(hide) :: nx
CF2PY integer, intent(hide) :: ny
CF2PY real, intent(in) :: dx
CF2PY real, intent(in) :: x(ny, nx)
CF2PY real, intent(out) :: ave(ny, nx)

      ! Local Variables
      integer :: i,j
!-----------------------------------------------------------------------!
!                          START OF SUBROUTINE                          !
!-----------------------------------------------------------------------!
      ave = 0.0
      do j=2,ny-1
        do i=2,nx-1
          ave(j, i) = 0.2*(x(j-1,i)+x(j,i-1)+x(j,i)+x(j,i+1)+x(j+1,i))
        end do
      end do

      end subroutine fivepointave
