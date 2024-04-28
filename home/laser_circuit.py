import sorter
from emitter import Emitter
from receiver import Receiver
from photon import Photon
from mirror import Mirror
from board_displayer import BoardDisplayer

'''
Name:   Javier Herrera Saavedra
SID:    540159552
Unikey: jher0112

LaserCircuit - Responsible for storing all the components of the circuit and
handling the computation of running the circuit. It's responsible for delegating 
tasks to the specific components e.g. making each emitter emit a photon, getting 
each photon to move and interact with components, etc. In general, this class is
responsible for handling any task related to the circuit.

You are free to add more attributes and methods, as long as you aren't 
modifying the existing scaffold.
'''


class LaserCircuit:

    def __init__(self, width: int, height: int, colour_frequency_ranges: dict = None):
        '''         
        Initialise a LaserCircuit instance given a width and height. All 
        lists of components and photons are empty by default.
        board_displayer is initialised to a BoardDisplayer instance. clock is
        0 by default.

        emitters:        list[Emitter]  - all emitters in this circuit
        receivers:       list[Receiver] - all receivers in this circuit
        photons:         list[Photon]   - all photons in this circuit
        mirrors:         list[Mirror]   - all mirrors in this circuit
        width:           int            - the width of this circuit board
        height:          int            - the height of this circuit board
        board_displayer: BoardDisplayer - helper class for storing and 
                                          displaying the circuit board
        clock:           int            - a clock keeping track of how many 
                                          nanoseconds this circuit has run for

        Parameters
        ----------
        width  - the width to set this circuit board to
        height - the width to set this circuit board to
        '''
        self.emitters: list[Emitter] = []
        self.receivers: list[Receiver] = []
        self.photons: list[Photon] = []
        self.mirrors: list[Mirror] = []
        self.width: int = width
        self.height: int = height
        self.colour_frequency_ranges: dict = colour_frequency_ranges
        self.board_displayer = BoardDisplayer(
            self.width, self.height, self.colour_frequency_ranges)
        self.clock: int = 0
        self.colour_mode: bool = isinstance(colour_frequency_ranges, dict)

    def emit_photons(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Gets each emitter in this circuit's list of emitters to emit a photon.
        The photons emitted should be added to this circuit's photons list.
        '''
        i = 0
        while i < len(self.get_emitters()):
            if self.colour_mode:
                self.board_displayer.change_emitter_format(self.get_emitters()[i], True)
            new_photon = self.get_emitters()[i].emit_photon()
            self.photons.append(new_photon)
            i += 1

    def is_finished(self) -> bool:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Returns whether or not this circuit has finished running. The
        circuit is finished running if every photon in the circuit has been
        absorbed.

        Returns
        -------
        True if the circuit has finished running or not, else False.
        '''
        photones_absorbed = 0
        i = 0
        while i < len(self.get_photons()):
            if self.get_photons()[i].is_absorbed():
                photones_absorbed += 1
            i += 1
        if len(self.get_photons()) == photones_absorbed:
            return True
        return False

    def print_emit_photons(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Prints the output for each emitter emitting a photon.

        It will also need to write the output into a
        /home/output/emit_photons.out output file. 

        You can assume the /home/output/ path exists.
        '''
        out_head_emitting = f"{self.clock}ns: Emitting photons."
        i = 0
        with open('home/output/emit_photons.out', 'w') as file:
            print(out_head_emitting)
            while i < len(self.get_emitters()):
                out_emitter = self.get_emitters()[i]
                print(out_emitter)
                file.write(str(out_emitter)+'\n')
                i += 1

    def print_activation_times(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Prints the output for the activation times for each receiver, sorted
        by activation time in ascending order. Any receivers that have not
        been activated should not be included.

        It will also need to write the output into a
        /home/output/activation_times.out output file.

        You can assume the /home/output/ path exists.
        '''
        activation_head = "Activation times:"
        # Sort by activation times
        self.receivers = sorter.sort_receivers_by_activation_time(
            self.receivers)
        with open('home/output/activation_times.out', 'w') as file:
            print(activation_head)
            i = 0
            while i < len(self.get_receivers()):
                out_receiver = self.get_receivers()[i]
                receiver_time = f"R{out_receiver.get_symbol()}: {out_receiver.get_activation_time()}ns"
                # Print when is activated
                if out_receiver.is_activated():
                    print(receiver_time)
                    file.write(str(receiver_time)+'\n')
                i += 1

    def print_total_energy(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Prints the output for the total energy absorbed for each receiver,
        sorted by total energy absorbed in descending order. Any receivers
        that have not been activated should not be included.

        It will also need to write the output into a
        /home/output/total_energy_absorbed.out output file.

        You can assume the /home/output/ path exists.
        '''
        out_head_received = f"Total energy absorbed:"
        self.receivers = sorter.sort_receivers_by_total_energy(self.receivers)
        with open('home/output/total_energy.out', 'w') as file:
            print(out_head_received)
            i = 0
            while i < len(self.get_receivers()):
                out_receiver = self.get_receivers()[i]
                if out_receiver.is_activated():
                    print(out_receiver)
                    file.write(str(out_receiver)+'\n')
                i += 1

    def print_board(self) -> None:
        '''Calls the print_board method in board_displayer.'''
        self.board_displayer.print_board()

    def get_collided_emitter(self, entity: Emitter | Receiver | Photon | Mirror) -> Emitter | None:
        '''
        Takes in one argument entity which is either a component or a photon
        and checks if it has the same position as another emitter in the 
        circuit. 

        If it does, return the emitter already in the entity's position.
        Else, return None, indicating there is no emitter occupying entity's
        position.

        Parameter
        ---------
        entity - an emitter, receiver, photon or mirror

        Returns
        -------
        An emitter if it has the same position as entity, else None.
        '''
        if len(self.emitters) > 0:
            i = 0
            while i < len(self.emitters):
                if self.emitters[i].get_x() == entity.get_x() and self.emitters[i].get_y() == entity.get_y():
                    return self.emitters[i]
                i += 1
        return None

    def get_collided_receiver(self, entity: Emitter | Receiver | Photon | Mirror) -> Receiver | None:
        '''
        Takes in one argument entity which is either a component or a photon
        and checks if it has the same position as another receiver in the 
        circuit. 

        If it does, return the receiver already in the entity's position.
        Else, return None, indicating there is no receiver occupying entity's
        position.

        Parameter
        ---------
        entity - an emitter, receiver, photon or mirror

        Returns
        -------
        A receiver if it has the same position as entity, else None.
        '''
        if len(self.receivers) > 0:
            i = 0
            while i < len(self.receivers):
                if self.receivers[i].get_x() == entity.get_x() and self.receivers[i].get_y() == entity.get_y():
                    return self.receivers[i]
                i += 1
        return None

    def get_collided_mirror(self, entity: Emitter | Receiver | Photon | Mirror) -> Mirror | None:
        # only requires implementation once you reach ADD-MY-MIRRORS
        '''
        Takes in one argument entity which is either a component or a photon
        and checks if it has the same position as another mirror in the 
        circuit. 

        If it does, return the mirror already in the entity's position.
        Else, return None, indicating there is no mirror occupying entity's
        position.

        Parameter
        ---------
        entity - an emitter, receiver, photon or mirror

        Returns
        -------
        A mirror if it has the same position as entity, else None.
        '''
        # remove the line below once you start implementing this function
        if len(self.mirrors) > 0:
            i = 0
            while i < len(self.mirrors):
                if self.mirrors[i].get_x() == entity.get_x() and self.mirrors[i].get_y() == entity.get_y():
                    return self.mirrors[i]
                i += 1
        return None

    def get_collided_component(self, photon: Photon) -> Emitter | Receiver | Mirror | None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        # will require extensions in ADD-MY-MIRRORS
        '''
        Given a photon, returns the component it has collided with (if any).
        A collision occurs if the positions of photon and the component are
        the same.

        Parameters
        ----------
        photon - a photon to check for collision with the circuit's components

        Returns
        -------
        If the photon collided with a component, return that component.
        Else, return None.

        Hint
        ----
        Use the three collision methods above to handle this.
        '''
        if isinstance(self.get_collided_receiver(photon), Receiver):
            return self.get_collided_receiver(photon)
        if isinstance(self.get_collided_emitter(photon), Emitter):
            return self.get_collided_emitter(photon)
        if isinstance(self.get_collided_mirror(photon), Mirror):
            return self.get_collided_mirror(photon)
        return None

    def tick(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Runs a single nanosecond (tick) of this circuit. If the circuit has
        already finished, this method should return out early.

        Otherwise, for each photon that has not been absorbed, this method is
        responsible for moving it, updating the board to show its new position
        and checking if it collided with a component (and handling it if did
        occur). At the end, we then increment clock.
        '''
        if not self.is_finished():
            self.clock += 1
            i = 0
            while i < len(self.photons):
                if not self.photons[i].is_absorbed():
                    self.photons[i].move(self.get_width(), self.get_height())
                    self.board_displayer.add_photon_to_board(
                        self.photons[i], self.colour_mode)
                    # check collision with component
                    component = self.get_collided_component(self.photons[i])
                    if component != None:
                        self.photons[i].interact_with_component(
                            component, self.clock)
                        # color
                        if self.colour_mode and isinstance(component, Receiver) and component.is_activated():
                            self.board_displayer.change_receiver_format(
                                component, component.is_activated())
                i += 1
        return

    def run_circuit(self) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Runs the entire circuit from start to finish. This involves getting
        each emitter to emit a photon, and continuously running tick until the
        circuit is finished running. All output in regards of running the 
        circuit should be contained in this method.
        '''
        head_print = """========================
   RUNNING CIRCUIT...
========================"""
        footer_print = """========================
   CIRCUIT FINISHED!
========================"""
        # Firstly
        print(head_print)
        print()

        if self.colour_mode:
            # change color emitter
            i = 0
            while i < len(self.get_emitters()):
                self.board_displayer.change_emitter_format(
                    self.get_emitters()[i], False)
                i += 1
            i = 0
            while i < len(self.get_receivers()):
                self.board_displayer.change_receiver_format(
                    self.get_receivers()[i], self.get_receivers()[i].is_activated())
                i += 1

        # Secondly
        self.emit_photons()
        self.print_emit_photons()
        print()

        # Thirdly
        total_receivers = len(self.get_receivers())
        while not self.is_finished():
            self.tick()
            self.tick()
            self.tick()
            self.tick()
            self.tick()
            # have to be distinct receivers
            i = 0
            activated_receivers = 0
            while i < total_receivers:
                if self.get_receivers()[i].is_activated():
                    activated_receivers += 1
                i += 1

            print(f"{self.clock}ns: {
                  activated_receivers}/{total_receivers} receiver(s) activated.")
            self.print_board()
            print()

        # Forthly
        self.print_activation_times()
        print()
        # Fifthly
        self.print_total_energy()
        print()
        # Lastly
        print(footer_print)

    def add_emitter(self, emitter: Emitter) -> bool:
        '''
        If emitter is not an Emitter instance, return False. Else, you need to
        perform the following checks in order for any errors:
          1)  The emitter's position is within the bounds of the circuit.
          2)  The emitter's position is not already taken by another emitter in
              the circuit.
          3)  The emitter's symbol is not already taken by another emitter in 
              the circuit.

        If at any point a check is not passed, an error message is printed
        stating the causeof the error and returns False, skipping any further
        checks. If all checks pass, then the following needs to occur:
          1)  emitter is added in the circuit's list of emitters. emitter
              needs to be added such that the list of emitters remains sorted
              in alphabetical order by the emitter's symbol. You can assume the
              list of emitters is already sorted before you add the emitter.
          2)  emitter's symbol is added into board_displayer.
          3)  The method returns True.   

        Parameters
        ----------
        emitter - the emitter to add into this circuit's list of emitters

        Returns
        ----------
        Returns true if all checks are passed and the emitter is added into
        the circuit.
        Else, if any of the checks are not passed, prints an error message
        stating the cause of the error and returns False, skipping any
        remaining checks.

        Hint
        ----
        Use the get_collided_emitter method to check for position collision.
        You will need to find your own way to check for symbol collisions
        with other emitters.
        '''
        # Check if emitter is instance of Emitter
        if not isinstance(emitter, Emitter):
            return False
        # Check 1: emitter is within the bounds of the circuit
        if not (0 <= emitter.get_x() < self.get_width()) and not (0 <= emitter.get_y() < self.get_height()):
            print("Error: position ({}, {}) is out-of-bounds of {}x{} circuit board".format(
                emitter.get_x(), emitter.get_y(), self.get_width(), self.get_height()))
            return False
        # Check 2: emitter position is not already taken by other emitter
        if self.get_collided_emitter(emitter):
            print("Error: position ({}, {}) is already taken by emitter '{}'".format(
                emitter.get_x(), emitter.get_y(), self.get_collided_emitter(emitter).get_symbol()))
            return False
        # Check 3: emitter symbol is not already taken by another emitter
        i = 0
        while i < len(self.emitters):
            if emitter.get_symbol() == self.emitters[i].get_symbol():
                print("Error: symbol '{}' is already taken".format(
                    emitter.get_symbol()))
                return False
            i += 1
        # If all test pass
        # Add emitter alphabetically
        self.emitters.append(emitter)
        # Sort
        self.emitters = sorter.sort_emitters_by_symbol(self.emitters)
        # Add to board BoardDisplayer
        self.board_displayer.add_component_to_board(emitter)
        # Return True
        return True

    def get_emitters(self) -> list[Emitter]:
        '''Returns emitters.'''
        return self.emitters

    def add_receiver(self, receiver: Receiver) -> bool:
        '''
        If receiver is not a Receiver instance, return False. Else, you need to
        perform the following checks in order for any errors:
          1)  The receiver's position is within the bounds of the circuit.
          2)  The receiver's position is not already taken by another emitter
              or receiver in the circuit.
          3)  The receiver's symbol is not already taken by another receiver in
              the circuit. 

        If at any point a check is not passed, an error message is printed stating
        the cause of the error and returns False, skipping any further checks. If 
        all checks pass, then the following needs to occur:
          1)  receiver is added in the circuit's list of receivers. receiver
              needs to be added such that the list of receivers  remains sorted
              in alphabetical order by the receiver's symbol. You can assume the
              list of receivers is already sorted before you add the receiver. 
          2)  receiver's symbol is added into board_displayer.
          3)  The method returns True.

        Parameters
        ----------
        receiver - the receiver to add into this circuit's list of receivers

        Returns
        ----------
        Returns true if all checks are passed and the receiver is added into
        the circuit.
        Else, if any of the checks are not passed, prints an error message
        stating the cause of the error and returns False, skipping any
        remaining checks.

        Hint
        ----
        Use the get_collided_emitter and get_collided_receiver methods to
        check for position collisions.
        You will need to find your own way to check for symbol collisions
        with other receivers.
        '''
        # Check if receiver is instance of Receiver
        if not isinstance(receiver, Receiver):
            return False
        # Check 1: receiver is within the bounds of the circuit
        if not (0 <= receiver.get_x() < self.get_width()) and not(0 <= receiver.get_y() < self.get_height()):
            print("Error: position ({}, {}) is out-of-bounds of {}x{} circuit board".format(
                receiver.get_x(), receiver.get_y(), self.get_width(), self.get_height()))
            return False
        # Check 2: receiver position is not already taken by other emitter
        if self.get_collided_emitter(receiver):
            print("Error: position ({}, {}) is already taken by emitter '{}'".format(
                receiver.get_x(), receiver.get_y(), self.get_collided_emitter(receiver).get_symbol()))
            return False
        # Check 3: receiver position is not already taken by other receiver
        if self.get_collided_receiver(receiver):
            print("Error: position ({}, {}) is already taken by receiver '{}'".format(
                receiver.get_x(), receiver.get_y(), self.get_collided_receiver(receiver).get_symbol()))
            return False
        # Check 4: receiver symbol is not already taken by another receiver
        i = 0
        while i < len(self.receivers):
            if receiver.get_symbol() == self.receivers[i].get_symbol():
                print("Error: symbol '{}' is already taken".format(
                    receiver.get_symbol()))
                return False
            i += 1
        # If all test pass
        # Add receiver alphabetically
        self.receivers.append(receiver)
        # Sort
        self.receivers = sorter.sort_receivers_by_symbol(self.receivers)
        self.board_displayer.add_component_to_board(receiver)
        # Return True
        return True

    def get_receivers(self) -> list[Receiver]:
        '''Returns receivers.'''
        return self.receivers

    def add_photon(self, photon: Photon) -> bool:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        If the photon passed in is not a Photon instance, it does not add it in
        and returns False. Else, it adds photon in this circuit's list of
        photons and returns True.

        Parameters
        ----------
        photon - the photon to add into this circuit's list of photons

        Returns
        -------
        Returns True if the photon is added in, else False.
        '''
        if type(photon) != Photon:
            return False
        else:
            self.photons.append(photon)
            return True

    def get_photons(self) -> list[Photon]:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''Returns photons.'''
        return self.photons

    def add_mirror(self, mirror: Mirror) -> bool:
        # only requires implementation once you reach ADD-MY-MIRRORS
        '''
        If mirror is not a Mirror instance, return False. Else, you need to
        perform the following checks in order for any errors:
          1)  The mirror's position is within the bounds of the circuit.
          2)  The mirror's position is not already taken by another emitter, 
              receiver or mirror in the circuit.

        If at any point a check is not passed, an error message is printed
        stating the cause of theerror and returns False, skipping any further
        checks. If all checks pass, then the following needs to occur: 
          1)  mirror is added in the circuit's list of mirrors.
          2) mirror's symbol is added into board_displayer.
          3)   The method returns True.

        Parameters
        ----------
        mirror - the mirror to add into this circuit's list of mirrors

        Returns
        ----------
        Returns true if all checks are passed and the mirror is added into
        the circuit.
        Else, if any of the checks are not passed, prints an error message
        stating the cause of the error and returns False, skipping any
        remaining checks.
        '''
        if type(mirror) != Mirror:
            return False
        if not ((mirror.get_x() >= 0 and mirror.get_x() < self.get_width()) and (mirror.get_y() >= 0 and mirror.get_y() < self.get_height())):
            print("Error: position ({}, {}) is out-of-bounds of {}x{} circuit board".format(
                mirror.get_x(), mirror.get_y(), self.get_width(), self.get_height()))
            return False
        if not self.get_collided_emitter(mirror) == None:
            print("Error: position ({}, {}) is already taken by emitter '{}'".format(
                mirror.get_x(), mirror.get_y(), self.get_collided_emitter(mirror).get_symbol()))
            return False
        if not self.get_collided_receiver(mirror) == None:
            print("Error: position ({}, {}) is already taken by receiver '{}'".format(
                mirror.get_x(), mirror.get_y(), self.get_collided_receiver(mirror).get_symbol()))
            return False
        if not self.get_collided_mirror(mirror) == None:
            print("Error: position ({}, {}) is already taken by mirror '{}'".format(
                mirror.get_x(), mirror.get_y(), self.get_collided_mirror(mirror).get_symbol()))
            return False

        self.mirrors.append(mirror)
        self.board_displayer.add_component_to_board(mirror)
        return True

    def get_mirrors(self) -> list[Mirror]:
        # only requires implementation once you reach ADD-MY-MIRRORS
        '''Returns mirrors.'''
        return self.mirrors

    def get_width(self) -> int:
        '''Returns width.'''
        return self.width

    def get_height(self) -> int:
        '''Returns height.'''
        return self.height
