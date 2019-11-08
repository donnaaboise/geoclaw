! qinit routine for parabolic bowl problem, only single layer
subroutine qinit(meqn,mbc,mx,my,xlower,ylower,dx,dy,q,maux,aux)

    use geoclaw_module, only: grav

    implicit none

    ! Subroutine arguments
    integer, intent(in) :: meqn,mbc,mx,my,maux
    real(kind=8), intent(in) :: xlower,ylower,dx,dy
    real(kind=8), intent(inout) :: q(meqn,1-mbc:mx+mbc,1-mbc:my+mbc)
    real(kind=8), intent(inout) :: aux(maux,1-mbc:mx+mbc,1-mbc:my+mbc)

    ! Parameters for problem
    real(kind=8), parameter :: a = 1.d0
    real(kind=8), parameter :: sigma = 0.5d0
    real(kind=8), parameter :: h0 = 0.1d0

    real(kind=8) :: amplitude, centerx, centery
    real(kind=8) :: radius, radius2, hump
    real(kind=8) :: xll,yll,xur, yur


    ! Other storage
    integer :: i,j
    real(kind=8) :: omega,x,y,eta

    real(kind=8) :: hin,hout,win, xlow,ylow

    real(kind=8) :: x0, y0, r0
    common /fdisc_com/ x0, y0, r0

    logical use_gaussian, use_disk
    data use_gaussian /.false./
    data use_disk /.true./
    
    omega = sqrt(2.d0 * grav * h0) / a

    xll = -120
    yll = -60
    xur = -60
    yur = 0

    centerx = xlower + mx/2.d0*dx
    centery = ylower + my/2.d0*dy

    !! Needed for fdisc (below)
    x0 = centerx
    y0 = centery
    r0 = 10

    amplitude = 0.1d0
    
    do i=1-mbc,mx+mbc
        x = xlower + (i - 0.5d0)*dx
        do j=1-mbc,my+mbc
            y = ylower + (j - 0.5d0) * dy

            if (use_gaussian) then
                radius2 = (x-centerx)**2+(y-centery)**2        
                radius = sqrt(radius2)
                hump = amplitude*exp(-.05d0*radius**2)   
            elseif (use_disk) then
                hin = 0.1d0
                hout = 0
                xlow = xlower + (i-1)*dx
                ylow = ylower + (j-1)*dy
                call cellave(xlow,ylow,dx,dy,win)
                hump = hin*win + hout*(1.d0-win)
            else
                !! No surface perturbation
                hump = 0
            endif

            q(1,i,j) = max(0.d0,hump - aux(1,i,j))
            q(2,i,j) = 0.d0
            q(3,i,j) = 0.d0
        enddo
    enddo
    
end subroutine qinit


double precision function fdisc(x,y)
    implicit none

    double precision x,y

    double precision r2

    real(kind=8) :: x0, y0, r0
    common /fdisc_com/ x0, y0, r0

    r2 = (x-x0)**2 + (y-y0)**2

    fdisc = r2 - r0**2
    return
end function fdisc

