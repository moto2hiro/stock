import * as AppConsts from '../../../AppConsts';

import {
  Button,
  ButtonGroup,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Grid,
  IconButton,
  MenuItem,
  Modal,
  Paper,
  Popover,
  Snackbar,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
} from '@material-ui/core';

import CloseIcon from '@material-ui/icons/Close';
import EditIcon from '@material-ui/icons/Edit';
import FormUtils from '../../../appUtils/FormUtils';
import HelpOutlineIcon from '@material-ui/icons/HelpOutline';
import NumberUtils from '../../../appUtils/NumberUtils';
import React from 'react';
import SaveIcon from '@material-ui/icons/Save';
import SearchIcon from '@material-ui/icons/Search';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  paper: {
    height: 400,
    width: '100%',
    overflow: 'auto',
    marginBottom: theme.spacing(2),
  },
  table: {
    minWidth: 650,
    tableLayout: 'fixed',
  },
  popover: {
    padding: theme.spacing(2),
    maxWidth: 200,
    wordWrap: 'break-word',
  },
  modal: {
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    position: 'absolute',
    width: 600,
    backgroundColor: theme.palette.background.paper,
    boxShadow: theme.shadows[5],
    padding: theme.spacing(4),
    outline: 'none',
  },
}));

export default function SymbolsMaintTemplate(state) {
  const classes = useStyles();
  const [popoverAnchorEl, setPopoverAnchorEl] = React.useState(null);
  const [isPopoverOpen, setPopoverOpen] = React.useState(false);
  const [popoverContent, setPopoverContent] = React.useState(false);
  const onOpenPopover = (content) => (event) => {
    setPopoverAnchorEl(event.currentTarget);
    setPopoverOpen((prev) => !prev);
    setPopoverContent(content);
  };
  const onClosePopover = (event) => {
    setPopoverAnchorEl(null);
    setPopoverOpen((prev) => !prev);
    setPopoverContent('');
  };

  return (
    <>
      <Grid container>
        <Grid item xs={12}>
          <Card>
            <CardHeader title='Stock Symbols'></CardHeader>
            <Divider light={true} />
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    name='query'
                    label='Search Symbol'
                    value={state.query}
                    onChange={state.onChangeQuery}
                    fullWidth
                    onKeyPress={state.onKeyPress}
                    InputProps={{
                      startAdornment: (
                        <>
                          <SearchIcon />
                        </>
                      ),
                    }}
                  ></TextField>
                </Grid>
                <Grid item xs={12} className='mb-0 pb-0'>
                  <Paper className={classes.paper}>
                    <Table className={classes.table} size='small' stickyHeader>
                      <TableHead>
                        <TableRow>
                          <TableCell>Id</TableCell>
                          <TableCell>Symbol</TableCell>
                          <TableCell>Name</TableCell>
                          <TableCell>Sector</TableCell>
                          <TableCell>Industry</TableCell>
                          <TableCell>
                            Archived
                            <IconButton
                              color='secondary'
                              onClick={onOpenPopover(
                                'Symbols that are no longer publicly traded. Excluded from Data Import.'
                              )}
                              className='p-0'
                            >
                              <HelpOutlineIcon />
                            </IconButton>
                          </TableCell>
                          <TableCell>
                            Excluded From Trade
                            <IconButton
                              color='secondary'
                              onClick={onOpenPopover(
                                'Symbols to exclude in Trade Suggestions and BackTests. These symbols will still be included in Data Imports.'
                              )}
                              className='p-0'
                            >
                              <HelpOutlineIcon />
                            </IconButton>
                          </TableCell>
                          <TableCell></TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {!state.symbolsInView.length ? (
                          <TableRow>
                            <TableCell colSpan={6} align='center'>
                              No results found.
                            </TableCell>
                          </TableRow>
                        ) : (
                          state.symbolsInView.map((s, idx) => {
                            return (
                              <TableRow key={idx}>
                                <TableCell align='left'>{s.id}</TableCell>
                                <TableCell align='left'>{s.symbol}</TableCell>
                                <TableCell align='left'>{s.name}</TableCell>
                                <TableCell align='left'>{s.sector}</TableCell>
                                <TableCell align='left'>{s.industry}</TableCell>
                                <TableCell align='left'>
                                  {NumberUtils.hasBit(s.status, AppConsts.SYMBOL_STATUS_ARCHIVED) ? 'true' : 'false'}
                                </TableCell>
                                <TableCell align='left'>
                                  {NumberUtils.hasBit(s.status, AppConsts.SYMBOL_STATUS_EXCLUDE_TRADE)
                                    ? 'true'
                                    : 'false'}
                                </TableCell>
                                <TableCell align='left'>
                                  <IconButton color='secondary' onClick={() => state.onClickEdit(s)} className='p-0'>
                                    <EditIcon />
                                  </IconButton>
                                </TableCell>
                              </TableRow>
                            );
                          })
                        )}
                      </TableBody>
                    </Table>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      <Popover
        anchorOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        open={isPopoverOpen}
        anchorEl={popoverAnchorEl}
        onClose={onClosePopover}
      >
        {<div className={classes.popover}>{popoverContent}</div>}
      </Popover>
      <Snackbar
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'left',
        }}
        open={state.is_snackbar_open}
        autoHideDuration={6000}
        onClose={state.onCloseSnackbar}
        message={<span>{state.snackbar_content}</span>}
        action={[
          <IconButton key='close' aria-label='Close' color='inherit' className='p-1' onClick={state.onCloseSnackbar}>
            <CloseIcon />
          </IconButton>,
        ]}
      />
      <Modal open={state.is_modal_open} onClose={state.onCloseModal}>
        <Card className={classes.modal}>
          <CardHeader title={`Edit-${state.request.id}-${state.request.symbol}`}></CardHeader>
          <Divider light={true} />
          <CardContent>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  name='name'
                  label='Name'
                  value={state.request.name}
                  onChange={state.onChangeRequest}
                  onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                  className='mb-2'
                  fullWidth
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  select
                  name='is_excluded_from_trade'
                  label='Excluded From Trade'
                  value={state.request.is_excluded_from_trade}
                  onChange={state.onChangeRequest}
                  onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                  className='mb-2'
                  fullWidth
                >
                  <MenuItem value={true}>True</MenuItem>
                  <MenuItem value={false}>False</MenuItem>
                </TextField>
              </Grid>
            </Grid>
          </CardContent>
          <CardContent>
            <Grid container>
              <Grid item xs={12}>
                <ButtonGroup fullWidth>
                  <Button
                    size='large'
                    variant='contained'
                    color='secondary'
                    onClick={() => state.onClickSave()}
                    disabled={state.is_processing}
                  >
                    <SaveIcon className={classes.extendedIcon} />
                    Save
                  </Button>
                </ButtonGroup>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Modal>
    </>
  );
}
