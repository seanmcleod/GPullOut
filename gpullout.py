import math
import matplotlib.pyplot as plt

g = 9.81

ktToms = 0.5144444444
msTokt = 1.0 / ktToms
mToft = 3.2808399

def magnitude(x, y):
    return math.sqrt(x*x + y*y)

def ramp(startVal, endVal, period, time):
    if(time > period):
        return endVal
    return startVal + ((endVal - startVal) / period) * time

# Setup graph
fig = plt.figure(1, figsize=(8.5, 8.5))
ax = plt.subplot(111)
ax.yaxis.grid(True)
ax.xaxis.grid(True)
ax.set_ylim(-8000, 0)
#ax.set_xlim(0)

Lg = 4.0 
Wg = 1.0
Dg = 0.1
Tg = 0.0

times = []
alts = []

def gPullOut(initialVelocity, initialFPA):
    t = 0
    dt = 0.1

    fpa = math.radians(initialFPA)

    Vx = initialVelocity * ktToms * math.cos(fpa)
    Vy = initialVelocity * ktToms * math.sin(fpa) * -1.0

    alt = 0

    times.clear()
    alts.clear()
    times.append(0)
    alts.append(0)

    # TEMP TODO
    #Lg = 1.0 * math.cos(fpa)

    while(fpa >= 0.0):
        # Ramp Lg
        Lg = ramp(0.86, 6.0, 2.5, t)

        # Forces into x and y components based on fpa
        FLx = Lg * math.sin(fpa)
        FLy = Lg * math.cos(fpa)

        FWx = 0.0
        FWy = -Wg

        FDx = -Dg * math.cos(fpa)
        FDy = Dg * math.sin(fpa)

        # Sum the forces in x and y
        Fx = FLx + FWx + FDx
        Fy = FLy + FWy + FDy

        # Integrate forces/acceleration to get delta velocity in x and y
        dVx = Fx * g * dt
        dVy = Fy * g * dt

        # Resultant velocities
        Vx = Vx + dVx
        Vy = Vy + dVy

        Vkt = magnitude(Vx, Vy) * msTokt

        # Integrate Vy to update altitude
        alt = alt + Vy * dt

        # Determine new fpa
        fpa = math.atan2(-Vy, Vx)

        # Increment time
        t = t + dt

        # Print some results
        print(math.degrees(fpa), alt*mToft, Vkt)

        #ax.scatter(t, alt*mToft)
        times.append(t)
        alts.append(alt*mToft)

    ax.plot(times, alts)

# Runs
#gPullOut(480, 45)
#gPullOut(540, 45)
#gPullOut(600, 45)

gPullOut(540, 30)
gPullOut(540, 45)
gPullOut(540, 60)
gPullOut(540, 89)

plt.show()

print("Finished")