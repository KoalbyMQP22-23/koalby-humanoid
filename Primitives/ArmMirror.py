from Primitives import KoalbyPrimitive


class ArmMirror(KoalbyPrimitive.Primitive):

    def __init__(self, left_arm_group, right_arm_group):
        super().__init__()  # inheritance
        self.motorPositionsDict = {}
        self.masterArm = left_arm_group
        self.followerArm = right_arm_group
        self.isActive = False

        # Set default to left arm for demo
        # if str(input('Which arm would you like to control?:')) == 'left':  # set controller arm and follower arm
        # self.masterArm = leftArmGroup
        # self.followerArm = rightArmGroup
        # else:
        #    self.masterArm = rightArmGroup
        #    self.followerArm = leftArmGroup

    def arm_mirror(self):
        master_positions = list()
        for motor in self.masterArm:  # log motor positions of controller arm
            master_positions.append(motor.get_position)
        for motor in self.followerArm:  # set motors in follower arm to positions of controller arm
            self.motorPositionsDict[motor.motorID] = master_positions[0]  # add motor pos to motor dict sent to robot
            master_positions.pop(0)

    def set_active(self):
        for motor in self.masterArm:  # set desired controller arm to be compliant for manual control
            motor.compliant_toggle(1)
        self.isActive = True

    def not_active(self):
        for motor in self.masterArm:  # set desired controller arm to be compliant for manual control
            motor.compliant_toggle(0)
        self.isActive = False
