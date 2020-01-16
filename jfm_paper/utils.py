def get_gktl_drag_trajectories(gktl_dir, T=0, dt=1, dtype=float):
    """Return a dataframe containing the drag as a function of time for
    all the copies in a GKTL run.
    By default the instantaneous drag is returned.
    An integration window T can be specified to return the time averaged drag instead.

    Parameters:
    -----------
    gktl_dir: str
    T: float, optional
    dt: float, optional
    dtype: type, optional

    Returns:
    --------
    df: pandas.core.DataFrame
    """
    gktl_params = get_gktl_parameters(gktl_dir)
    Nc = gktl_params["nc"]
    traj_files = [
        os.path.join(gktl_dir, "recon_rep_0_clone_{}.traj".format(j)) for j in range(Nc)
    ]

    # Get size of trajectories
    nt = check_files(traj_files, dtype)

    traj_array = np.zeros((nt, Nc))

    for j, filename in enumerate(traj_files):
        traj_array[:, j] = np.fromfile(filename, dtype, -1, "")

    if T:
        npoints_avg_window = int(T / dt)
        df = pd.DataFrame(traj_array).rolling(npoints_avg_window).mean().dropna()
    else:
        df = pd.DataFrame(traj_array)

    return df

def write_reconstructed_trajectories(
        path_to_dir, br_end=-1, br_start=0, reps=-1, dtype=float, dt=1, dolastcloning=True, verbose=False
):

    gktl_params = get_gktl_parameters(path_to_dir)

    labels_file_path = os.path.join(path_to_dir, "labels.datout")
    labels = np.fromfile(labels_file_path, np.int32, -1, "")

    # Optional parameters
    nb_steps = gktl_params["Ta"] // gktl_params["DT"]
    if br_end == -1:
        br_end = nb_steps-1

    if reps == -1:
        reps = range(gktl_params["nrep"])

    nc = gktl_params["nc"]
    transient = gktl_params["transient"]
    npoints = int(gktl_params["DT"] / dt)

    def _get_previous_chunck(step, ancestor_idx):
        traj_file_name = "rep_{}_clone_{}.traj".format(rep, ancestor_idx)
        traj_file_path = os.path.join(path_to_dir, traj_file_name)
        offset = (transient + step * npoints) * np.dtype(
            dtype
        ).itemsize
        with open(traj_file_path, "rb") as f:
            f.seek(offset)
            previous_chunck = np.fromfile(f, float, npoints, "")

        return previous_chunck

    for rep in reps:
        if verbose:
            print("Reconstrucing trajectories for repetitions {}.".format(rep))
        rep_offset = nc * rep * nb_steps
        for j in range(nc):
            # Get first chunck of trajectory, starting from the endpoint.
            # Ancestors are trajectories themselves.
            if dolastcloning:
                ll = labels[
                    rep_offset + br_end * nc : rep_offset + (br_end+1) * nc
                ]
                ancestor_idx = ll[j]
            else:
                ancestor_idx = j

            recon_array = _get_previous_chunck(br_end, ancestor_idx)

            # Now repeat the same operation on the nb_steps-1, nb_steps-2.. chuncks.
            # Each time getting ancestor from label array
            for step in range(br_start, br_end)[::-1]:
                # The `labels` array contains the ancestor indexes for all
                # repetitions.
                # So must offset to get labels for current rep with `rep_offset`
                ll = labels[
                    rep_offset
                    + (step) * nc : rep_offset
                    + (step+1) * nc
                ]
                ancestor_idx = ll[ancestor_idx]
                x = _get_previous_chunck(step, ancestor_idx)
                recon_array = np.concatenate((x, recon_array))

            recon_traj_file_name = "recon_rep_{}_clone_{}.traj".format(rep, j)
            recon_traj_file_path = os.path.join(path_to_dir, recon_traj_file_name)
            with open(recon_traj_file_path, "wb") as f:
                recon_array.tofile(f)

def gktl_group_trajectories(gktl_dir, br_end, br_start, rep=0, dolastcloning=False):
    """Return sets of sampled trajectories which share a common ancestor at
    branching point br_start, ending at br_end.
    Parameters:
    -----------
    gktl_dir: str
    br_end: int
    br_start: int
    rep: int, optional
    dolastcloning: bool, optional

    Returns:
    --------
    dict_of_parents: dict of sets
    """

    gktl_params = get_gktl_parameters(gktl_dir)

    labels_file_path = os.path.join(gktl_dir, "labels.datout")
    labels = np.fromfile(labels_file_path, np.int32, -1, "")

    nb_steps = br_end - br_start + 1
    nc = gktl_params["nc"]

    dict_of_parents = {}
    rep_offset = nc * rep * nb_steps
    for j in range(nc):
        # Get first chunck of trajectory, starting from the endpoint.
        # Ancestors are trajectories themselves.
        if dolastcloning:
            ll = labels[
                rep_offset + br_end * nc : rep_offset + (br_end+1) * nc
            ]
            ancestor_idx = ll[j]
        else:
            ancestor_idx = j

            # Now repeat the same operation on the nb_steps-1, nb_steps-2.. chuncks.
            # Each time getting ancestor from label array
            for step in range(br_start, br_end)[::-1]:
                # The `labels` array contains the ancestor indexes for all
                # repetitions.
                # So must offset to get labels for current rep with `rep_offset`
                ll = labels[
                    rep_offset
                    + (step) * nc : rep_offset
                    + (step + 1) * nc
                ]
                ancestor_idx = ll[ancestor_idx]

        if ancestor_idx in dict_of_parents:
            dict_of_parents[ancestor_idx].append(j)
        else:
            dict_of_parents[ancestor_idx] = [j]

    return dict_of_parents

def _get_ancestor_idx(current_idx, labels, rep_offset, step, nc):
    # The `labels` array contains the ancestor indexes for all
    # repetitions.
    # So must offset to get labels for current rep with `rep_offset`
    ll = labels[
        rep_offset
        + (step) * nc : rep_offset
        + (step+1) * nc
    ]
    return ll[current_idx]

def gktl_reconstruct_trajectories(gktl_dir, br_end=1, br_start=0, rep=0, dolastcloning=False):
    gktl_params = get_gktl_parameters(path_to_dir)

    labels_file_path = os.path.join(path_to_dir, "labels.datout")
    labels = np.fromfile(labels_file_path, np.int32, -1, "")

    # Optional parameters
    nb_steps = gktl_params["Ta"] // gktl_params["DT"]
    if br_end == -1:
        br_end = nb_steps-1
    nc = gktl_params["nc"]

    rep_offset = nc * rep * nb_steps
    history = []
    for j in range(nc):
        history_backards = []
        # Get first chunck of trajectory, starting from the endpoint.
        # Ancestors are trajectories themselves.
        if dolastcloning:
            ancestor_idx = _get_ancestor_idx[j]
        else:
            ancestor_idx = j
        history_backwards.append(ancestor_idx)

        # Now repeat the same operation on the nb_steps-1, nb_steps-2.. chuncks.
        # Each time getting ancestor from label array
        for step in range(br_start, br_end)[::-1]:
            ancestor_idx = _get_ancestor_idx[ancestor_idx]
            history_backards.append(ancestor_idx)

        history[j] = history_backwards[::-1]

    return history
